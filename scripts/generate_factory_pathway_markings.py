
#!/usr/bin/env python3

from pathlib import Path
import sys
import numpy as np
import trimesh
from shapely.geometry import Point
from shapely.ops import unary_union

# Import the exact V6 route geometry.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_factory_pathways_v6 import (
    make_network,
    create_export_geometry,
    geometry_components,
)

OUTPUT = Path("/tmp/sentra_factory_pathway_markings.stl")

# V6 pathway dimensions
PATH_BOTTOM = 0.005
PATH_HEIGHT = 0.040
PATH_TOP = PATH_BOTTOM + PATH_HEIGHT

# Marking dimensions
MARKING_WIDTH = 0.07
MARKING_HEIGHT = 0.002
MARKING_INSET = 0.045

# Roundabout settings
ROUNDABOUT_CENTER = (0.0, 5.0)
ROUNDABOUT_RADIUS = 4.5





def create_marking_geometry(network):
    """Generate edge bands using inward polygon erosion."""

    # Create an inward-offset pathway surface.
    inner_network = network.buffer(
        -MARKING_WIDTH,
        quad_segs=16,
        join_style="round",
    )

    # Edge bands are the difference between the original
    # pathway surface and its inward-offset version.
    markings = network.difference(inner_network)

    # Exclude the central roundabout.
    roundabout = Point(
        *ROUNDABOUT_CENTER
    ).buffer(
        ROUNDABOUT_RADIUS - 0.05,
        quad_segs=128,
    )

    
    markings = markings.difference(roundabout)
    markings = markings.buffer(0)

    # Remove small isolated marking fragments.
    components = geometry_components(markings)

    MIN_MARKING_AREA = 0.25

    retained = [
        polygon
        for polygon in components
        if polygon.area >= MIN_MARKING_AREA
    ]

    if not retained:
        raise RuntimeError("All marking components were removed.")

    markings = unary_union(retained).buffer(0)

    print("Original components:", len(components))
    print("Retained components:", len(retained))
    print("Removed components:", len(components) - len(retained))
    print("Final marking area:", round(markings.area, 3), "m²")

    return markings


def create_marking_mesh(geometry):
    """Create planar visual-only marking surfaces."""

    meshes = []

    marking_z = PATH_BOTTOM + PATH_HEIGHT + 0.002

    for polygon in geometry_components(geometry):

        if polygon.area <= 1e-8:
            continue

        vertices, faces = trimesh.creation.triangulate_polygon(
            polygon,
            engine="earcut",
        )

        # Convert 2D coordinates (X,Y) into 3D (X,Y,Z).
        vertices_3d = np.column_stack([
            vertices,
            np.full(len(vertices), marking_z),
        ])

        mesh = trimesh.Trimesh(
            vertices=vertices_3d,
            faces=faces,
            process=True,
        )

        meshes.append(mesh)

    if not meshes:
        raise RuntimeError("No marking surfaces generated.")

    return trimesh.util.concatenate(meshes)




def main():

    print("\nSENTRA PATHWAY MARKINGS GENERATOR")
    print("=================================")

    network = make_network()

    network = create_export_geometry(network)

    markings = create_marking_geometry(network)

    mesh = create_marking_mesh(markings)

    print("\n===== MARKING VALIDATION =====")
    print("Geometry valid:", markings.is_valid)
    print("Marking area:", round(markings.area, 3), "m²")
    print("Watertight:", mesh.is_watertight)
    print("Vertices:", len(mesh.vertices))
    print("Faces:", len(mesh.faces))
    print("Bounds:", mesh.bounds)

    if not markings.is_valid:
        raise RuntimeError("Invalid marking geometry.")

    if len(mesh.faces) == 0:
        raise RuntimeError("Marking mesh has no faces.")

    if not mesh.is_winding_consistent:
        raise RuntimeError("Marking mesh has inconsistent face winding.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    mesh.export(str(OUTPUT))

    print("\nMARKING EXPORT COMPLETE")
    print("Output:", OUTPUT)


if __name__ == "__main__":
    main()

