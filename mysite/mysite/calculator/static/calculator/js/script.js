'use strict';

 function appendValue(value) {
            document.getElementById("result").value += value;
        }

        function calculateResult() {
            var expression = document.getElementById("result").value;
            try {
                var result = eval(expression);
                document.getElementById("result").value = result;
            } catch (error) {
                document.getElementById("result").value = "Error";
            }
        }

        function clearResult() {
            document.getElementById("result").value = "";
        }