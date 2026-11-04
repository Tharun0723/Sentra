
cmake_minimum_required(VERSION 3.8)
project(sentra_gazebo)

find_package(ament_cmake REQUIRED)

# Install simulation configuration, launch files and Gazebo worlds.
install(
  DIRECTORY config launch worlds
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

