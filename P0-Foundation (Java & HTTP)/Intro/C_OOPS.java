class keyBoard{
    int keyCount;
    String name;
    String color;
    int price = 1500;

    public void type()
    {
        System.out.println("Keyboard is typing");
    }

    public void throwIt(){
        System.out.println("Keyboard is thrown");
    }
}


// This is an example of inheritance in Java where the child class (AdvancedKeyBoard) inherits the properties and methods of the parent class (keyBoard)

class AdvancedKeyBoard extends keyBoard{
    public void wireless()
    {
        System.out.println("This is a wireless keyboard");
    }
}

public class C_OOPS{
    public static void main(String[] args) {
        System.out.println("OOPS Concepts in Java");
        
        
        int keyCount = 104; // variable
        
        keyBoard k1; // proccess of creating an object
        k1 = new keyBoard(); // This is a constructor which is used to  initialize the object

        AdvancedKeyBoard ak1 = new AdvancedKeyBoard(); // This is a constructor which is used to  initialize the object of the child class and it will also call the constructor of the parent class

        // All of this constructor creation and object creation could be done in one line as follows:
        // keyBoard k1 = new keyBoard();

        k1.keyCount = keyCount;
        k1.name = "Logitech";
        k1.color = "White";
        // k1.price = 2000; // This will override the price of the keyboard which is set in the class as 1500 and it will be set to 2000 but if we do not set the price of the keyboard then it will take the price from the class which is 1500
        
        System.out.println("Keyboard Name: " + k1.name);
        System.out.println("Keyboard Color: " + k1.color);
        System.out.println("Keyboard Price: " + k1.price); // Accessing the properties of the class using the object of the class and in terms of precedence the object of the class is given more precedence than the variable of the same name

        // The methods of the class can be called using the object of the class
        k1.type();
        k1.throwIt();


        ak1.throwIt(); // This will call the method of the parent class
        ak1.type(); // This will call the method of the parent class    
        ak1.wireless(); // This will call the method of the child class
    }
}