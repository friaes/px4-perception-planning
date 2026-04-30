// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from detection_msgs:msg/Detection2D.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "detection_msgs/msg/detection2_d.hpp"


#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__TRAITS_HPP_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "detection_msgs/msg/detail/detection2_d__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace detection_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Detection2D & msg,
  std::ostream & out)
{
  out << "{";
  // member: x_min
  {
    out << "x_min: ";
    rosidl_generator_traits::value_to_yaml(msg.x_min, out);
    out << ", ";
  }

  // member: y_min
  {
    out << "y_min: ";
    rosidl_generator_traits::value_to_yaml(msg.y_min, out);
    out << ", ";
  }

  // member: x_max
  {
    out << "x_max: ";
    rosidl_generator_traits::value_to_yaml(msg.x_max, out);
    out << ", ";
  }

  // member: y_max
  {
    out << "y_max: ";
    rosidl_generator_traits::value_to_yaml(msg.y_max, out);
    out << ", ";
  }

  // member: class_name
  {
    out << "class_name: ";
    rosidl_generator_traits::value_to_yaml(msg.class_name, out);
    out << ", ";
  }

  // member: class_id
  {
    out << "class_id: ";
    rosidl_generator_traits::value_to_yaml(msg.class_id, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Detection2D & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x_min
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x_min: ";
    rosidl_generator_traits::value_to_yaml(msg.x_min, out);
    out << "\n";
  }

  // member: y_min
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y_min: ";
    rosidl_generator_traits::value_to_yaml(msg.y_min, out);
    out << "\n";
  }

  // member: x_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x_max: ";
    rosidl_generator_traits::value_to_yaml(msg.x_max, out);
    out << "\n";
  }

  // member: y_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y_max: ";
    rosidl_generator_traits::value_to_yaml(msg.y_max, out);
    out << "\n";
  }

  // member: class_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "class_name: ";
    rosidl_generator_traits::value_to_yaml(msg.class_name, out);
    out << "\n";
  }

  // member: class_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "class_id: ";
    rosidl_generator_traits::value_to_yaml(msg.class_id, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Detection2D & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace detection_msgs

namespace rosidl_generator_traits
{

[[deprecated("use detection_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const detection_msgs::msg::Detection2D & msg,
  std::ostream & out, size_t indentation = 0)
{
  detection_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use detection_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const detection_msgs::msg::Detection2D & msg)
{
  return detection_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<detection_msgs::msg::Detection2D>()
{
  return "detection_msgs::msg::Detection2D";
}

template<>
inline const char * name<detection_msgs::msg::Detection2D>()
{
  return "detection_msgs/msg/Detection2D";
}

template<>
struct has_fixed_size<detection_msgs::msg::Detection2D>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<detection_msgs::msg::Detection2D>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<detection_msgs::msg::Detection2D>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__TRAITS_HPP_
