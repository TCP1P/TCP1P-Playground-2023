#!/bin/env python3

class run():
  def __init__(self) -> None:
    pass
  def r(self):
    code = input("input your code: ")
    if any([(i in code) for i in ["(", " "]]):
      return
    print(eval(code))

run().r()
