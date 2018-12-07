py_runtime(
    name = "python-3.5.3",
    files = [],
    interpreter_path = "/usr/bin/python3",
)

py_library(
    name = "model",
    srcs = ["model.py"],
    deps = [],
)

py_test(
    name = "model_test",
    srcs = ["model_test.py"],
    deps = [
      ":model",
    ],
)
