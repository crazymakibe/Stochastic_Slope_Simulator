cmake_minimum_required(VERSION 3.10)
project(JoshimathSolver)


find_package(deal.II 9.5.1 REQUIRED)
find_package(GDAL REQUIRED)


add_executable(joshimath_solver src/main.cpp src/slope_stability.cpp)


deal_ii_setup_target(joshimath_solver DEBUG)


target_include_directories(joshimath_solver PRIVATE ${GDAL_INCLUDE_DIRS})
target_link_libraries(joshimath_solver ${GDAL_LIBRARIES})