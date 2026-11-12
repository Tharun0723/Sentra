
#!/usr/bin/env python3

from pathlib import Path
import math

import trimesh
from shapely.geometry import LineString, Point, box
from shapely.ops import unary_union

# SENTRA FACTORY PATHWAY GENERATOR V6

OUTPUT = Path("/tmp/sentra_factory_pathways_v6.stl")

FLOOR = box(-20.0, -15.0, 20.0, 15.0)
WALL_MARGIN = 0.10

PRIMARY_WIDTH = 3.0
SECONDARY_WIDTH = 2.5

PATH_BOTTOM = 0.005
PATH_HEIGHT = 0.040

PILLAR_HALF_SIZE = 0.20
PILLAR_CLEARANCE = 0.50

PILLARS = [
    (x, y)
    for y in (-10.0, 0.0, 10.0)
    for x in (-15.0, -5.0, 5.0, 15.0)
]

ROUNDABOUT_CENTER = (0.0, 5.0)
ROUNDABOUT_RADIUS = 4.5
ISLAND_RADIUS = 1.5

OUTPUT = Path("/tmp/sentra_factory_pathways_v6.stl")

# ------------------------------------------------------------
# ROUTE CENTRE-LINES
# Each segment is straight unless an ARC is explicitly defined.
# ------------------------------------------------------------

ROUTES = [
    {
        "name": "south_main_approach",
        "width": PRIMARY_WIDTH,
        "segments": [
            ("LINE", [(0, -13.3), (0, 0.8)]),
        ],
    },
    {
        "name": "north_main_approach",
        "width": PRIMARY_WIDTH,
        "segments": [
            ("LINE", [(0, 9.2), (0, 13.0)]),
        ],
    },
    {
        "name": "west_roundabout_approach",
        "width": PRIMARY_WIDTH,
        "segments": [
            ("LINE", [(-18, 5), (-4.2, 5)]),
        ],
    },
    {
        "name": "east_roundabout_approach",
        "width": PRIMARY_WIDTH,
        "segments": [
            ("LINE", [(4.2, 5), (18, 5)]),
        ],
    },

    
    # Production — north-west
    {
        "name": "production_outer_loop",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(-8, 7), (-10, 7), (-16, 7)]),
            ("ARC", {"center": (-16, 9), "radius": 2,
                     "start": -90, "end": -180}),
            ("LINE", [(-18, 9), (-18, 11)]),
            ("ARC", {"center": (-16, 11), "radius": 2,
                     "start": 180, "end": 90}),
            ("LINE", [(-16, 13), (-10, 13)]),
            ("ARC", {"center": (-10, 11), "radius": 2,
                     "start": 90, "end": 0}),
            ("LINE", [(-8, 11), (-8, 9)]),
            ("ARC", {"center": (-10, 9), "radius": 2,
                     "start": 0, "end": -90}),
            ("LINE", [(-10, 7), (-8, 7)]),
        ],
    },

    # Machinery — north-east
    {
        "name": "machinery_outer_loop",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(8, 7), (10, 7), (16, 7)]),
            ("ARC", {"center": (16, 9), "radius": 2,
                     "start": -90, "end": 0}),
            ("LINE", [(18, 9), (18, 11)]),
            ("ARC", {"center": (16, 11), "radius": 2,
                     "start": 0, "end": 90}),
            ("LINE", [(16, 13), (10, 13)]),
            ("ARC", {"center": (10, 11), "radius": 2,
                     "start": 90, "end": 180}),
            ("LINE", [(8, 11), (8, 9)]),
            ("ARC", {"center": (10, 9), "radius": 2,
                     "start": 180, "end": 270}),
            ("LINE", [(10, 7), (8, 7)]),
        ],
    },

    # Warehouse — south-west
    {
        "name": "warehouse_outer_loop",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(-8, -7), (-10, -7), (-16, -7)]),
            ("ARC", {"center": (-16, -9), "radius": 2,
                     "start": 90, "end": 180}),
            ("LINE", [(-18, -9), (-18, -11)]),
            ("ARC", {"center": (-16, -11), "radius": 2,
                     "start": 180, "end": 270}),
            ("LINE", [(-16, -13), (-10, -13)]),
            ("ARC", {"center": (-10, -11), "radius": 2,
                     "start": 270, "end": 360}),
            ("LINE", [(-8, -11), (-8, -9)]),
            ("ARC", {"center": (-10, -9), "radius": 2,
                     "start": 0, "end": 90}),
            ("LINE", [(-10, -7), (-8, -7)]),
        ],
    },

    # Loading and dispatch — south-east
    {
        "name": "dispatch_outer_loop",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(8, -7), (10, -7), (16, -7)]),
            ("ARC", {"center": (16, -9), "radius": 2,
                     "start": 90, "end": 0}),
            ("LINE", [(18, -9), (18, -11)]),
            ("ARC", {"center": (16, -11), "radius": 2,
                     "start": 0, "end": -90}),
            ("LINE", [(16, -13), (10, -13)]),
            ("ARC", {"center": (10, -11), "radius": 2,
                     "start": 270, "end": 180}),
            ("LINE", [(8, -11), (8, -9)]),
            ("ARC", {"center": (10, -9), "radius": 2,
                     "start": 180, "end": 90}),
            ("LINE", [(10, -7), (8, -7)]),
        ],
    },


    # Purposeful cross-zone connectors
    {
        "name": "west_zone_connector",
        "width": PRIMARY_WIDTH,
        "segments": [
            ("LINE", [(-8, 7), (-8, -7)]),
        ],
    },
    
    {
        "name": "east_zone_connector",
        "width": PRIMARY_WIDTH,
        "segments": [
            ("LINE", [(8, 7), (8, -7)]),
        ],
    },

    # ========================================================
    # A — PRODUCTION: internal inspection network
    # ========================================================

    {
        "name": "production_internal_spine",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(-11.5, 7), (-11.5, 13)]),
        ],
    },
    {
        "name": "production_cross_aisle",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(-11.5, 10), (-8, 10)]),
        ],
    },

    # ========================================================
    # B — MACHINERY: internal inspection network
    # ========================================================

    {
        "name": "machinery_internal_spine",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(11.5, 7), (11.5, 13)]),
        ],
    },
    {
        "name": "machinery_cross_aisle",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(11.5, 10), (8, 10)]),
        ],
    },

    # ========================================================
    # C — WAREHOUSE: internal inspection network
    # ========================================================

    {
        "name": "warehouse_internal_spine",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(-11.5, -13), (-11.5, -7)]),
        ],
    },
    {
        "name": "warehouse_cross_aisle",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(-11.5, -10), (-8, -10)]),
        ],
    },

    # ========================================================
    # D — LOADING & DISPATCH: internal inspection network
    # ========================================================

    {
        "name": "dispatch_internal_spine",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(11.5, -13), (11.5, -7)]),
        ],
    },
    {
        "name": "dispatch_cross_aisle",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(11.5, -10), (8, -10)]),
        ],
    },

    
    # Lower-middle factory cross-zone connector
    {
        "name": "lower_middle_cross_connector",
        "width": PRIMARY_WIDTH,
        "segments": [
            ("LINE", [(-8, -4.5), (8, -4.5)]),
        ],
    },


    # Top connection between production and machinery
    {
        "name": "upper_zone_connector",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(-10, 13), (10, 13)]),
        ],
    },

    # Left-side connection between west routes
    {
        "name": "west_outer_connector",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(-18, 7), (-18, -7)]),
        ],
    },

    # Right-side connection between east routes
    {
        "name": "east_outer_connector",
        "width": SECONDARY_WIDTH,
        "segments": [
            ("LINE", [(18, 7), (18, -7)]),
        ],
    },



]



def arc_points(center, radius, start_deg, end_deg):
    """Create a smooth circular arc using exact-radius samples."""
    cx, cy = center

    if radius <= 0:
        raise ValueError("Arc radius must be positive.")

    sweep = end_deg - start_deg
    steps = max(12, math.ceil(abs(sweep) / 3))

    return [
        (
            cx + radius * math.cos(
                math.radians(start_deg + sweep * i / steps)
            ),
            cy + radius * math.sin(
                math.radians(start_deg + sweep * i / steps)
            ),
        )
        for i in range(steps + 1)
    ]


def build_route_segments(route):
    """Convert explicit line and arc definitions into centrelines."""
    pieces = []

    for kind, data in route["segments"]:
        if kind == "LINE":
            points = data
        elif kind == "ARC":
            points = arc_points(
                data["center"],
                data["radius"],
                data["start"],
                data["end"],
            )
        else:
            raise ValueError(f"Unknown segment type: {kind}")

        if len(points) < 2:
            raise ValueError(f"Invalid segment in {route['name']}")

        pieces.append(LineString(points))

    # Validate intentional continuity between consecutive pieces.
    for first, second in zip(pieces, pieces[1:]):
        if first.distance(second) > 1e-5:
            raise ValueError(
                f"Disconnected line/arc transition in {route['name']}"
            )

    return pieces


def route_surface(route):
    """Buffer route centrelines into a controlled-width surface."""
    surfaces = []

    for line in build_route_segments(route):
        surfaces.append(
            line.buffer(
                route["width"] / 2,
                quad_segs=16,
                cap_style="flat",
                join_style="round",
            )
        )

    return unary_union(surfaces)


# ============================================================
# NETWORK ASSEMBLY
# ============================================================

def make_network():
    """Combine all intentionally designed route surfaces."""
    surfaces = []

    for route in ROUTES:
        print(f"Building route: {route['name']}")
        surfaces.append(route_surface(route))

    network = unary_union(surfaces)

    if network.is_empty:
        raise RuntimeError("Pathway network is empty.")

    return network


# ============================================================
# PILLAR CLEARANCE
# ============================================================

def make_pillar_obstacles():
    obstacles = []

    for x, y in PILLARS:
        footprint = box(
            x - PILLAR_HALF_SIZE,
            y - PILLAR_HALF_SIZE,
            x + PILLAR_HALF_SIZE,
            y + PILLAR_HALF_SIZE,
        )

        obstacles.append(
            footprint.buffer(PILLAR_CLEARANCE)
        )

    return obstacles


# ============================================================
# GEOMETRY COMPONENTS
# ============================================================

def geometry_components(geometry):
    if geometry.is_empty:
        return []

    if geometry.geom_type == "Polygon":
        return [geometry]

    if geometry.geom_type == "MultiPolygon":
        return list(geometry.geoms)

    return [
        item for item in getattr(geometry, "geoms", [])
        if item.geom_type == "Polygon"
    ]


# ============================================================
# VALIDATION
# ============================================================

def validate_geometry(network):
    print("\n===== V6 GEOMETRY VALIDATION =====")

    allowed_floor = FLOOR.buffer(-WALL_MARGIN)
    boundary_ok = allowed_floor.covers(network)

    print("Inside factory boundary:", boundary_ok)

    conflicts = []

    for index, obstacle in enumerate(make_pillar_obstacles(), 1):
        if network.intersects(obstacle):
            conflicts.append(index)

    print(
        "Pillar clearance:",
        "PASS" if not conflicts else "FAIL"
    )
    print("Pillar conflicts:", conflicts if conflicts else "None")

    print("Path geometry valid:", network.is_valid)

    cx, cy = ROUNDABOUT_CENTER

    roundabout = Point(cx, cy).buffer(
        ROUNDABOUT_RADIUS,
        quad_segs=128,
    )

    logical_network = unary_union([
        network,
        roundabout,
    ])

    components = geometry_components(logical_network)

    print(
        "Connected components including roundabout:",
        len(components)
    )

    island = Point(cx, cy).buffer(ISLAND_RADIUS)

    island_clear = (
        network.intersection(island).area <= 1e-6
    )

    print(
        "Central island clearance:",
        "PASS" if island_clear else "FAIL"
    )

    if not boundary_ok:
        raise RuntimeError("Pathways exceed factory boundary.")

    if conflicts:
        raise RuntimeError(
            f"Pillar clearance conflicts: {conflicts}"
        )

    if not network.is_valid:
        raise RuntimeError("Invalid pathway geometry.")

    if len(components) != 1:
        raise RuntimeError(
            "Disconnected pathway network, including roundabout."
        )

    if not island_clear:
        raise RuntimeError("Pathways overlap central island.")

    print("V6 GEOMETRY VALIDATION PASSED")


# ============================================================
# ROUNDABOUT CUTOUT
# ============================================================

def create_export_geometry(network):
    """Keep the existing roundabout model separate."""
    cx, cy = ROUNDABOUT_CENTER

    roundabout_disk = Point(cx, cy).buffer(
        ROUNDABOUT_RADIUS,
        quad_segs=128,
    )

    return network.difference(roundabout_disk)


# ============================================================
# STL MESH GENERATION
# ============================================================

def create_mesh(geometry):
    polygons = geometry_components(geometry)

    meshes = []

    for polygon in polygons:
        if polygon.area <= 1e-8:
            continue

        mesh = trimesh.creation.extrude_polygon(
            polygon,
            height=PATH_HEIGHT,
            engine="earcut",
        )

        mesh.apply_translation([
            0,
            0,
            PATH_BOTTOM,
        ])

        meshes.append(mesh)

    if not meshes:
        raise RuntimeError("No pathway mesh generated.")

    return trimesh.util.concatenate(meshes)


# ============================================================
# MAIN
# ============================================================

def main():
    print("\nSENTRA FACTORY PATHWAY GENERATOR V6")
    print("===================================")

    network = make_network()

    validate_geometry(network)

    export_geometry = create_export_geometry(network)

    mesh = create_mesh(export_geometry)

    print("\n===== V6 MESH REPORT =====")
    print("Watertight:", mesh.is_watertight)
    print("Vertices:", len(mesh.vertices))
    print("Faces:", len(mesh.faces))
    print(
        "Mesh components:",
        len(mesh.split(only_watertight=False))
    )
    print("Bounds:", mesh.bounds)

    if not mesh.is_watertight:
        raise RuntimeError("Generated mesh is not watertight.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    mesh.export(str(OUTPUT))

    print("\n===== V6 EXPORT COMPLETE =====")
    print("Output:", OUTPUT)
    print("Routes:", len(ROUTES))
    print("Pillars checked:", len(PILLARS))
    print("Equipment clearance: Pending")
    print("Gazebo integration: Not performed")


if __name__ == "__main__":
    main()
