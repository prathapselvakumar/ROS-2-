cmake_minimum_required(VERSION 3.8)
project(custom_message_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_cmake REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CustomMessage.msg"
)

ament_package()
