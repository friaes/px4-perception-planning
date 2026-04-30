// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from detection_msgs:msg/Detection2DArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "detection_msgs/msg/detection2_d_array.hpp"


#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__STRUCT_HPP_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'detections'
#include "detection_msgs/msg/detail/detection2_d__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__detection_msgs__msg__Detection2DArray __attribute__((deprecated))
#else
# define DEPRECATED__detection_msgs__msg__Detection2DArray __declspec(deprecated)
#endif

namespace detection_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Detection2DArray_
{
  using Type = Detection2DArray_<ContainerAllocator>;

  explicit Detection2DArray_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->inference_latency_ms = 0.0f;
      this->total_latency_ms = 0.0f;
      this->fps = 0.0f;
    }
  }

  explicit Detection2DArray_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->inference_latency_ms = 0.0f;
      this->total_latency_ms = 0.0f;
      this->fps = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _detections_type =
    std::vector<detection_msgs::msg::Detection2D_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<detection_msgs::msg::Detection2D_<ContainerAllocator>>>;
  _detections_type detections;
  using _inference_latency_ms_type =
    float;
  _inference_latency_ms_type inference_latency_ms;
  using _total_latency_ms_type =
    float;
  _total_latency_ms_type total_latency_ms;
  using _fps_type =
    float;
  _fps_type fps;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__detections(
    const std::vector<detection_msgs::msg::Detection2D_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<detection_msgs::msg::Detection2D_<ContainerAllocator>>> & _arg)
  {
    this->detections = _arg;
    return *this;
  }
  Type & set__inference_latency_ms(
    const float & _arg)
  {
    this->inference_latency_ms = _arg;
    return *this;
  }
  Type & set__total_latency_ms(
    const float & _arg)
  {
    this->total_latency_ms = _arg;
    return *this;
  }
  Type & set__fps(
    const float & _arg)
  {
    this->fps = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    detection_msgs::msg::Detection2DArray_<ContainerAllocator> *;
  using ConstRawPtr =
    const detection_msgs::msg::Detection2DArray_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<detection_msgs::msg::Detection2DArray_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<detection_msgs::msg::Detection2DArray_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      detection_msgs::msg::Detection2DArray_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<detection_msgs::msg::Detection2DArray_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      detection_msgs::msg::Detection2DArray_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<detection_msgs::msg::Detection2DArray_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<detection_msgs::msg::Detection2DArray_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<detection_msgs::msg::Detection2DArray_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__detection_msgs__msg__Detection2DArray
    std::shared_ptr<detection_msgs::msg::Detection2DArray_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__detection_msgs__msg__Detection2DArray
    std::shared_ptr<detection_msgs::msg::Detection2DArray_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Detection2DArray_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->detections != other.detections) {
      return false;
    }
    if (this->inference_latency_ms != other.inference_latency_ms) {
      return false;
    }
    if (this->total_latency_ms != other.total_latency_ms) {
      return false;
    }
    if (this->fps != other.fps) {
      return false;
    }
    return true;
  }
  bool operator!=(const Detection2DArray_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Detection2DArray_

// alias to use template instance with default allocator
using Detection2DArray =
  detection_msgs::msg::Detection2DArray_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace detection_msgs

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__STRUCT_HPP_
