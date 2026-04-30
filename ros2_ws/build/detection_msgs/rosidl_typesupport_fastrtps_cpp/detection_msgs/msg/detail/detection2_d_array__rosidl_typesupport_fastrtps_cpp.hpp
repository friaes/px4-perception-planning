// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from detection_msgs:msg/Detection2DArray.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include <cstddef>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "detection_msgs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "detection_msgs/msg/detail/detection2_d_array__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace detection_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_detection_msgs
cdr_serialize(
  const detection_msgs::msg::Detection2DArray & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_detection_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  detection_msgs::msg::Detection2DArray & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_detection_msgs
get_serialized_size(
  const detection_msgs::msg::Detection2DArray & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_detection_msgs
max_serialized_size_Detection2DArray(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_detection_msgs
cdr_serialize_key(
  const detection_msgs::msg::Detection2DArray & ros_message,
  eprosima::fastcdr::Cdr &);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_detection_msgs
get_serialized_size_key(
  const detection_msgs::msg::Detection2DArray & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_detection_msgs
max_serialized_size_key_Detection2DArray(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace detection_msgs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_detection_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, detection_msgs, msg, Detection2DArray)();

#ifdef __cplusplus
}
#endif

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
