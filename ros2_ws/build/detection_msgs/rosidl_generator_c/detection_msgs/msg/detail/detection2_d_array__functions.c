// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from detection_msgs:msg/Detection2DArray.idl
// generated code does not contain a copyright notice
#include "detection_msgs/msg/detail/detection2_d_array__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `detections`
#include "detection_msgs/msg/detail/detection2_d__functions.h"

bool
detection_msgs__msg__Detection2DArray__init(detection_msgs__msg__Detection2DArray * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    detection_msgs__msg__Detection2DArray__fini(msg);
    return false;
  }
  // detections
  if (!detection_msgs__msg__Detection2D__Sequence__init(&msg->detections, 0)) {
    detection_msgs__msg__Detection2DArray__fini(msg);
    return false;
  }
  // inference_latency_ms
  // total_latency_ms
  // fps
  return true;
}

void
detection_msgs__msg__Detection2DArray__fini(detection_msgs__msg__Detection2DArray * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // detections
  detection_msgs__msg__Detection2D__Sequence__fini(&msg->detections);
  // inference_latency_ms
  // total_latency_ms
  // fps
}

bool
detection_msgs__msg__Detection2DArray__are_equal(const detection_msgs__msg__Detection2DArray * lhs, const detection_msgs__msg__Detection2DArray * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // detections
  if (!detection_msgs__msg__Detection2D__Sequence__are_equal(
      &(lhs->detections), &(rhs->detections)))
  {
    return false;
  }
  // inference_latency_ms
  if (lhs->inference_latency_ms != rhs->inference_latency_ms) {
    return false;
  }
  // total_latency_ms
  if (lhs->total_latency_ms != rhs->total_latency_ms) {
    return false;
  }
  // fps
  if (lhs->fps != rhs->fps) {
    return false;
  }
  return true;
}

bool
detection_msgs__msg__Detection2DArray__copy(
  const detection_msgs__msg__Detection2DArray * input,
  detection_msgs__msg__Detection2DArray * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // detections
  if (!detection_msgs__msg__Detection2D__Sequence__copy(
      &(input->detections), &(output->detections)))
  {
    return false;
  }
  // inference_latency_ms
  output->inference_latency_ms = input->inference_latency_ms;
  // total_latency_ms
  output->total_latency_ms = input->total_latency_ms;
  // fps
  output->fps = input->fps;
  return true;
}

detection_msgs__msg__Detection2DArray *
detection_msgs__msg__Detection2DArray__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  detection_msgs__msg__Detection2DArray * msg = (detection_msgs__msg__Detection2DArray *)allocator.allocate(sizeof(detection_msgs__msg__Detection2DArray), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(detection_msgs__msg__Detection2DArray));
  bool success = detection_msgs__msg__Detection2DArray__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
detection_msgs__msg__Detection2DArray__destroy(detection_msgs__msg__Detection2DArray * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    detection_msgs__msg__Detection2DArray__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
detection_msgs__msg__Detection2DArray__Sequence__init(detection_msgs__msg__Detection2DArray__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  detection_msgs__msg__Detection2DArray * data = NULL;

  if (size) {
    data = (detection_msgs__msg__Detection2DArray *)allocator.zero_allocate(size, sizeof(detection_msgs__msg__Detection2DArray), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = detection_msgs__msg__Detection2DArray__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        detection_msgs__msg__Detection2DArray__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
detection_msgs__msg__Detection2DArray__Sequence__fini(detection_msgs__msg__Detection2DArray__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      detection_msgs__msg__Detection2DArray__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

detection_msgs__msg__Detection2DArray__Sequence *
detection_msgs__msg__Detection2DArray__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  detection_msgs__msg__Detection2DArray__Sequence * array = (detection_msgs__msg__Detection2DArray__Sequence *)allocator.allocate(sizeof(detection_msgs__msg__Detection2DArray__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = detection_msgs__msg__Detection2DArray__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
detection_msgs__msg__Detection2DArray__Sequence__destroy(detection_msgs__msg__Detection2DArray__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    detection_msgs__msg__Detection2DArray__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
detection_msgs__msg__Detection2DArray__Sequence__are_equal(const detection_msgs__msg__Detection2DArray__Sequence * lhs, const detection_msgs__msg__Detection2DArray__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!detection_msgs__msg__Detection2DArray__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
detection_msgs__msg__Detection2DArray__Sequence__copy(
  const detection_msgs__msg__Detection2DArray__Sequence * input,
  detection_msgs__msg__Detection2DArray__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(detection_msgs__msg__Detection2DArray);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    detection_msgs__msg__Detection2DArray * data =
      (detection_msgs__msg__Detection2DArray *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!detection_msgs__msg__Detection2DArray__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          detection_msgs__msg__Detection2DArray__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!detection_msgs__msg__Detection2DArray__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
