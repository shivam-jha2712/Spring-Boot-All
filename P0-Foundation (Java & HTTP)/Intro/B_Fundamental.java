public class B_Fundamental {
    
    public static void main(String[] args) {
        int num1 = 5;
        int num2 = 9;

        // Arithmetic Operators
        int sum = num1 + num2; // Addition 
        int difference = num1 - num2; // Subtraction
        int product = num1 * num2; // Multiplication
        int quotient = num1 / num2; // Division
        int remainder = num1 % num2; // Modulus
        System.out.println("Sum: " + sum);
        System.out.println("Difference: " + difference);
        System.out.println("Product: " + product);
        System.out.println("Quotient: " + quotient);
        System.out.println("Remainder: " + remainder);

        // Relational Operators
        boolean isGreater = num1 > num2;
        boolean isLess = num1 < num2;
        boolean isEqual = num1 == num2;
        boolean isNotEqual = num1 != num2;
        boolean isGreaterOrEqual = num1 >= num2;
        boolean isLessOrEqual = num1 <= num2;

        System.out.println("Is " + num1 + " greater than " + num2 + "? " + isGreater);
        System.out.println("Is " + num1 + " less than " + num2 + "? " + isLess);
        System.out.println("Is " + num1 + " equal to " + num2 + "? " + isEqual);
        System.out.println("Is " + num1 + " not equal to " + num2 + "? " + isNotEqual);
        System.out.println("Is " + num1 + " greater than or equal to " + num2 + "? " + isGreaterOrEqual);
        System.out.println("Is " + num1 + " less than or equal to " + num2 + "? " + isLessOrEqual);

        // Logical Operators
        boolean a = true;
        boolean b = false;      

        boolean andResult = a && b;
        boolean orResult = a || b;
        boolean notResult = !a;

        System.out.println("AND result: " + andResult);
        System.out.println("OR result: " + orResult);
        System.out.println("NOT result: " + notResult);

        // Assignment Operators
        int x = 10;
        x += 5; // x = x + 5    
        System.out.println("After += 5: " + x);
        x -= 3; // x = x - 3
        System.out.println("After -= 3: " + x);

        // Increment and Decrement Operators
        int count = 0;
        count++; // count = count + 1
        System.out.println("After increment: " + count);
        count--; // count = count - 1
        System.out.println("After decrement: " + count);

        // Ternary Operator
        int max = (num1 > num2) ? num1 : num2;  
        System.out.println("Maximum of " + num1 + " and " + num2 + " is: " + max);

        // Bitwise Operators
        int bitwiseAnd = num1 & num2; // Bitwise AND
        int bitwiseOr = num1 | num2; // Bitwise OR
        int bitwiseXor = num1 ^ num2; // Bitwise XOR
        int leftShift = num1 << 1; // Left shift by 1 position
        int rightShift = num2 >> 1; // Right shift by 1 position

        System.out.println("Bitwise AND: " + bitwiseAnd);
        System.out.println("Bitwise OR: " + bitwiseOr);
        System.out.println("Bitwise XOR: " + bitwiseXor);
        System.out.println("Left Shift of " + num1 + ": " + leftShift);
        System.out.println("Right Shift of " + num2 + ": " + rightShift);

        // Operator Precedence
        int result = num1 + num2 * 2; // Multiplication has higher precedence  
        System.out.println("Result of num1 + num2 * 2: " + result);
        result = (num1 + num2) * 2; // Parentheses change precedence
        System.out.println("Result of (num1 + num2) * 2: " + result);

        // Type Casting
        double d = 3.14;
        int i = (int) d; // Explicit casting from double to int
        System.out.println("Value of d: " + d);
        System.out.println("Value of i (casted from d): " + i);

        // Auto-boxing and Unboxing
        Integer numObj = num1; // Auto-boxing: int to Integer   
        int numPrimitive = numObj; // Unboxing: Integer to int
        System.out.println("Auto-boxed Integer: " + numObj);
        System.out.println("Unboxed int: " + numPrimitive);

        // String Concatenation
        String str1 = "Hello";
        String str2 = "World";
        String message = str1 + " " + str2; // Concatenation using +
        System.out.println("Concatenated String: " + message);

        // for loop
        for (int i1 = 1; i1 <= 5; i1++) {
            System.out.println("Loop iteration: " + i1);
        }

        // while loop
        int count1 = 1;
        while (count1 <= 5) {
            System.out.println("While loop count: " + count1);
            count1++;
        }

        // do-while loop
        int count2 = 1;
        do {
            System.out.println("Do-while loop count: " + count2);
            count2++;
        } while (count2 <= 5);



    }
}
