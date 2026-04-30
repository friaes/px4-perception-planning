// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from detection_msgs:msg/Detection2D.idl
// generated code does not contain a copyright notice
#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "detection_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "detection_msgs/msg/detail/detection2_d__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
bool cdr_serialize_detection_msgs__msg__Detection2D(
  const detection_msgs__msg__Detection2D * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
bool cdr_deserialize_detection_msgs__msg__Detection2D(
  eprosima::fastcdr::Cdr &,
  detection_msgs__msg__Detection2D * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
size_t get_serialized_size_detection_msgs__msg__Detection2D(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
size_t max_serialized_size_detection_msgs__msg__Detection2D(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
bool cdr_serialize_key_detection_msgs__msg__Detection2D(
  const detection_msgs__msg__Detection2D * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
size_t get_serialized_size_key_detection_msgs__msg__Detection2D(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
size_t max_serialized_size_key_detection_msgs__msg__Detection2D(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, detection_msgs, msg, Detection2D)();

#ifdef __cplusplus
}
#endif

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
