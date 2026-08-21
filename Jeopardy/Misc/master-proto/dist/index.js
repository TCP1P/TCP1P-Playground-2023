// index.ts
import vm from "vm";
var input = prompt("Input: ");
var result = vm.runInNewContext(input);
if (result?.result) {
  result.result = {};
}
