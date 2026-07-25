# Libraries + Frameworks inside a stage frame. Shows: frame-grows-to-fit,
# two parents in one column, and 3rd-level sub-branches.
# frame [id] title=<key>   encloses all nodes (or contains=a,b for a subset).

frame [f5] title=stage5

[libraries] grade=junior
  [boost]      grade=middle
  [opencv]     grade=optional
  [poco]       grade=optional
  [protobuf]   grade=optional
  [grpc]       grade=optional
    [asio]     grade=optional
  [fmt]        grade=optional
  [pybind11]   grade=optional
    [njson]    grade=optional
  [spdlog]     grade=optional
  [rangev3]    grade=optional
  [tensorflow] grade=optional
  [opencl]     grade=optional

[frameworks] grade=junior
  [gtest]     grade=middle
  [qt]        grade=optional
  [catch2]    grade=optional
    [gbench]  grade=optional
  [gprofiler] grade=optional
  [pytorch]   grade=optional
