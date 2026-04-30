// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from detection_msgs:msg/Detection2DArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "detection_msgs/msg/detection2_d_array.hpp"


#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__TRAITS_HPP_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "detection_msgs/msg/detail/detection2_d_array__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'detections'
#include "detection_msgs/msg/detail/detection2_d__traits.hpp"

namespace detection_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Detection2DArray & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: detections
  {
    if (msg.detections.size() == 0) {
      out << "detections: []";
    } else {
      out << "detections: [";
      size_t pending_items = msg.detections.size();
      for (auto item : msg.detections) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: inference_latency_ms
  {
    out << "inference_latency_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.inference_latency_ms, out);
    out << ", ";
  }

  // member: total_latency_ms
  {
    out << "total_latency_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.total_latency_ms, out);
    out << ", ";
  }

  // member: fps
  {
    out << "fps: ";
    rosidl_generator_traits::value_to_yaml(msg.fps, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Detection2DArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: detections
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.detections.size() == 0) {
      out << "detections: []\n";
    } else {
      out << "detections:\n";
      for (auto item : msg.detections) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: inference_latency_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "inference_latency_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.inference_latency_ms, out);
    out << "\n";
  }

  // member: total_latency_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "total_latency_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.total_latency_ms, out);
    out << "\n";
  }

  // member: fps
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fps: ";
    rosidl_generator_traits::value_to_yaml(msg.fps, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Detection2DArray & msg, bool use_flow_style = false)
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
  const detection_msgs::msg::Detection2DArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  detection_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use detection_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const detection_msgs::msg::Detection2DArray & msg)
{
  return detection_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<detection_msgs::msg::Detection2DArray>()
{
  return "detection_msgs::msg::Detection2DArray";
}

template<>
inline const char * name<detection_msgs::msg::Detection2DArray>()
{
  return "detection_msgs/msg/Detection2DArray";
}

template<>
struct has_fixed_size<detection_msgs::msg::Detection2DArray>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<detection_msgs::msg::Detection2DArray>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<detection_msgs::msg::Detection2DArray>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__TRAITS_HPP_
