/*
 Demonstration of different ways to provide an implementation for a
 single-method interface (`Walkable`) in Java:
  1) Concrete class that implements the interface (`WalkFast`).
  2) Anonymous inner class providing the implementation inline.
  3) Lambda expression (concise form for functional interfaces).
*/
public class MainClass {
    public static void main(String[] args) {

        // 1) Older Way: instantiate a concrete class that implements Walkable.
        // This uses a named class (`WalkFast`) which implements the method.
        Walkable walkFast = new WalkFast();
        System.out.println(walkFast.walk(10)); // prints 20

        // 2) Anonymous inner class: provide an implementation inline
        // without creating a separate named class.
        Walkable walkFastAnonymous = new Walkable() {
            @Override
            public int walk(int steps) {
                // Inline implementation inside the anonymous class
                return steps * 2;
            }
        };
        System.out.println(walkFastAnonymous.walk(10)); // prints 20

        // 3) New Way using Lambda Expression:
        // Lambdas provide a concise way to implement a functional interface
        // (an interface with a single abstract method). The parameter type
        // can be inferred, so we only write `(steps) -> steps * 2`.
        Walkable walkFastLambda = (steps) -> steps * 2;
        System.out.println(walkFastLambda.walk(10)); // prints 20

    }
}

// `Walkable` is a functional interface: it has a single abstract method.
// You can optionally annotate it with @FunctionalInterface to enforce
// the single-method rule at compile time.
interface Walkable {
    int walk(int steps);
}

// Concrete implementation of Walkable using a regular class.
class WalkFast implements Walkable {
    @Override
    public int walk(int steps) {
        // Simple implementation that multiplies steps by 2 to simulate
        // walking faster.
        return steps * 2;
    }
} 