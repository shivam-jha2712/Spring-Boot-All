# Knowledge Pool

This file is automatically maintained by the
[`update-knowledge-pool`](.github/workflows/update-knowledge-pool.yml)
GitHub Actions workflow.

Each entry is generated on every push to `master`, summarising the Spring Boot,
Java, and general programming concepts introduced in that commit. The script
scans both **code patterns** (annotations, APIs) and **code comments** (shorthand
notes, questions, explanations) to detect concepts.

---

## Entry #1 — 2026-02-22 | Commit: `fb79ee7` — Merge pull request #3 from shivam-jha2712/copilot/check-docs-creation-status

> **Author:** Shivam Jha

### Concepts Introduced

#### Spring Boot Auto-Configuration & Application Bootstrap

`@SpringBootApplication` is a convenience meta-annotation that combines `@Configuration`, `@EnableAutoConfiguration`, and `@ComponentScan`. It marks the main class of a Spring Boot application, triggers classpath scanning for beans, and enables opinionated auto-configuration so that sensible infrastructure defaults are applied without any manual bean declarations.

**References:**
- [Spring Boot Reference — @SpringBootApplication](https://docs.spring.io/spring-boot/docs/current/reference/html/using.html#using.using-the-springbootapplication-annotation)
- [Spring Boot Auto-Configuration Classes](https://docs.spring.io/spring-boot/docs/current/reference/html/auto-configuration-classes.html)

#### Spring MVC REST Controller

`@RestController` is a stereotype annotation that combines `@Controller` and `@ResponseBody`. Every method in a `@RestController` class automatically serialises its return value (typically to JSON via Jackson) and writes it directly to the HTTP response body, bypassing view resolution entirely.

**References:**
- [Spring API — @RestController](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RestController.html)
- [Spring Guide: Building a RESTful Web Service](https://spring.io/guides/gs/rest-service/)

#### Spring MVC Request Mapping

Request-mapping annotations (`@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`) are composed shorthand forms of `@RequestMapping` pre-bound to a specific HTTP method. They map a handler method to a URL path and HTTP verb, enabling clean, RESTful endpoint declarations with minimal boilerplate.

**References:**
- [Spring MVC Reference — Request Mapping](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#mvc-ann-requestmapping)
- [Baeldung: Spring @RequestMapping Guide](https://www.baeldung.com/spring-requestmapping)

#### Spring Stereotype Annotations & Bean Registration

`@Service`, `@Component`, and `@Repository` mark classes as Spring-managed beans discovered automatically during component scanning. `@Repository` additionally enables persistence-exception translation, converting vendor-specific data-access exceptions into Spring's unified `DataAccessException` hierarchy.

**References:**
- [Spring Core — Stereotype Annotations](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-stereotype-annotations)
- [Baeldung: @Component vs @Repository vs @Service](https://www.baeldung.com/spring-component-repository-service)

#### Spring Boot Testing Slices

Spring Boot's test slices load only a relevant portion of the application context to keep tests fast. `@SpringBootTest` loads the full context; `@WebMvcTest` loads only the web layer; `@DataJpaTest` loads only JPA components. `MockMvc` enables controller testing without a running server, and `@MockBean` replaces a real bean with a Mockito mock.

**References:**
- [Spring Boot Test Auto-Configuration](https://docs.spring.io/spring-boot/docs/current/reference/html/test-auto-configuration.html)
- [Baeldung: Testing in Spring Boot](https://www.baeldung.com/spring-boot-testing)

#### Spring Dependency Injection

Spring resolves and injects dependencies automatically. `@Autowired` injects by type; constructor injection (the recommended approach) makes dependencies explicit and allows fields to be `final`, improving testability and preventing null-injection bugs.

**References:**
- [Spring Core — Dependency Injection](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-dependency-injection)
- [Baeldung: Constructor Injection in Spring](https://www.baeldung.com/constructor-injection-in-spring)

#### Spring Boot Conditional Bean Configuration

Spring Boot conditional annotations control whether a bean is registered based on runtime conditions. `@ConditionalOnProperty` activates a bean only when a specific property matches a given value — ideal for switching between implementations (e.g., payment providers) via `application.properties`. `@ConditionalOnBean` and `@ConditionalOnMissingBean` check for the presence or absence of other beans in the context.

**References:**
- [Spring Boot — Condition Annotations](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-auto-configuration.condition-annotations)
- [Baeldung: @ConditionalOnProperty Guide](https://www.baeldung.com/spring-conditionalonproperty)

#### Spring Boot Application Startup Runners

`CommandLineRunner` and `ApplicationRunner` are functional interfaces whose `run` method is invoked once the `ApplicationContext` is fully initialised. They are used to execute one-time startup logic — such as seeding a database, warming a cache, or verifying external services — without resorting to `@PostConstruct` or static initialiser blocks.

**References:**
- [Spring Boot Reference — CommandLineRunner](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.spring-application.command-line-runner)
- [Baeldung: Running Logic on Startup in Spring](https://www.baeldung.com/running-setup-logic-on-startup-in-spring)

#### Java Servlet Fundamentals

Java Servlets are the foundation of server-side web development in Java. `HttpServlet` processes HTTP requests via `doGet`/`doPost` methods. `HttpServletRequest` and `HttpServletResponse` provide access to request parameters, headers, cookies, and sessions. `RequestDispatcher` enables server-side forwarding between servlets. Understanding servlets is key to appreciating what Spring MVC abstracts away.

**References:**
- [Jakarta Servlet 6.0 Specification](https://jakarta.ee/specifications/servlet/6.0/)
- [Baeldung: Introduction to Java Servlets](https://www.baeldung.com/intro-to-servlets)

#### Servlet Session Management & Cookies

HTTP is stateless; `HttpSession` and `Cookie` are the two primary mechanisms for maintaining state across requests. `HttpSession` stores data server-side and tracks users via a `JSESSIONID` cookie. Cookies store small key-value pairs on the client browser. Understanding these primitives is essential before adopting Spring Session or Spring Security's session management.

**References:**
- [Jakarta Servlet Specification — Sessions](https://jakarta.ee/specifications/servlet/6.0/)
- [Baeldung: Cookies and Session in Servlets](https://www.baeldung.com/java-servlet-cookies-session)

#### Inversion of Control (IoC) & Interface-based Design

Inversion of Control is the core principle behind Spring's DI container. Instead of a class creating its own dependencies, the framework injects them. Programming to interfaces (e.g., a `PaymentService` interface with multiple implementations) enables loose coupling: the consuming class depends only on the contract, and the concrete implementation is selected at runtime by the Spring container.

**References:**
- [Spring Core — IoC Container Introduction](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-introduction)
- [Baeldung: IoC and DI in Spring](https://www.baeldung.com/inversion-control-and-dependency-injection-in-spring)

#### Java Inheritance & the `extends` Keyword

Inheritance lets a **child class** (`extends`) reuse and specialise the fields and methods of a **parent class**. The child inherits all non-private members and can override methods to provide its own implementation. `super` refers to the parent instance — used to call the parent constructor or an overridden method. Java supports single class inheritance but multiple interface implementation.

**References:**
- [Oracle Java Tutorials — Inheritance](https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html)
- [Baeldung: Guide to Inheritance in Java](https://www.baeldung.com/java-inheritance)

#### Java Interfaces & Abstract Classes

An **interface** defines a contract — method signatures without implementation (plus `default` methods since Java 8). A class `implements` one or more interfaces, promising to provide the method bodies. An **abstract class** sits between a concrete class and an interface: it can hold state and concrete methods but cannot be instantiated. Use interfaces for capability contracts and abstract classes for shared base behaviour.

**References:**
- [Oracle Java Tutorials — Interfaces](https://docs.oracle.com/javase/tutorial/java/IandI/createinterface.html)
- [Baeldung: Interface vs Abstract Class](https://www.baeldung.com/java-interface-vs-abstract-class)

#### Method Overriding in Java

When a subclass provides its own version of a method already defined in its parent, it **overrides** that method. The `@Override` annotation is optional but strongly recommended — the compiler will flag an error if the annotated method does not actually override a superclass method, catching typos and signature mismatches early. At runtime, the JVM uses dynamic dispatch to call the overridden version.

**References:**
- [Oracle Java Tutorials — Overriding Methods](https://docs.oracle.com/javase/tutorial/java/IandI/override.html)
- [Baeldung: Method Overriding in Java](https://www.baeldung.com/java-method-overriding)

#### Tight vs Loose Coupling

**Tight coupling** means a class directly creates or depends on a concrete implementation (e.g., `new RazorpayPaymentService()`). Changing the dependency forces changes in the consumer. **Loose coupling** means the consumer depends on an *abstraction* (interface), and the concrete implementation is supplied externally — typically via dependency injection. Loose coupling improves testability, swappability, and maintainability.

**References:**
- [Baeldung: Tight and Loose Coupling in Java](https://www.baeldung.com/java-coupling-classes-tight-loose)
- [Wikipedia: Coupling (Computer Programming)](https://en.wikipedia.org/wiki/Coupling_(computer_programming))

#### Inversion of Control (IoC)

**IoC** flips the traditional flow of control: instead of *your* code creating dependencies, a **container** (the Spring `ApplicationContext`) creates them and *injects* them into your objects. This is the foundational principle behind Spring's dependency injection. Your classes declare *what* they need (via constructor parameters, `@Autowired`, or `@Inject`); the container decides *how* and *when* to fulfil those needs.

**References:**
- [Spring Core — IoC Container](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-introduction)
- [Martin Fowler: Inversion of Control](https://martinfowler.com/bliki/InversionOfControl.html)
- [Baeldung: IoC and DI in Spring](https://www.baeldung.com/inversion-control-and-dependency-injection-in-spring)

#### Spring Beans & the Bean Lifecycle

A **bean** is any object managed by the Spring IoC container. Beans are created (instantiated), configured (dependencies injected), initialised (`@PostConstruct`), and eventually destroyed (`@PreDestroy`). By default beans are **singletons** — one instance per application context. Marking a class with `@Component`, `@Service`, `@Repository`, or defining it in a `@Configuration` class registers it as a bean.

**References:**
- [Spring Core — Bean Overview](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-definition)
- [Baeldung: What is a Spring Bean?](https://www.baeldung.com/spring-bean)

#### Spring Component Scanning

Component scanning is the mechanism by which Spring automatically discovers classes annotated with `@Component` (and its stereotypes `@Service`, `@Repository`, `@Controller`) on the classpath and registers them as beans. `@SpringBootApplication` implicitly enables scanning from the package it lives in downward, so any annotated class in a sub-package is automatically picked up.

**References:**
- [Spring Core — Classpath Scanning](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-classpath-scanning)
- [Baeldung: Spring Component Scanning](https://www.baeldung.com/spring-component-scanning)

#### Dependency Injection Styles: Constructor vs Field vs Setter

Spring supports three injection styles:

• **Constructor injection** (recommended) — dependencies are passed via the constructor; fields can be `final`, making the object immutable and easy to test.
• **Setter injection** — dependencies are set via public setter methods after construction.
• **Field injection** (`@Autowired` on a field) — convenient but prevents `final` fields, hides dependencies from the public API, and makes unit testing harder without a DI container.

The Spring team officially recommends constructor injection.

**References:**
- [Spring Core — Setter-based DI](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-setter-injection)
- [Baeldung: Constructor Injection in Spring](https://www.baeldung.com/constructor-injection-in-spring)

#### Spring ApplicationContext

The `ApplicationContext` is the central interface of the Spring IoC container. It loads bean definitions, wires dependencies, manages the bean lifecycle, and publishes application events. `SpringApplication.run(...)` in a Spring Boot app creates and refreshes an `ApplicationContext`, making all declared beans available for injection.

**References:**
- [Spring Core — ApplicationContext](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#context-introduction)
- [Baeldung: ApplicationContext in Spring](https://www.baeldung.com/spring-application-context)

#### Java Type Casting

Java supports two kinds of type conversion:

• **Widening (implicit)** — smaller type → larger type (`int` → `double`) — no data loss, done automatically.
• **Narrowing (explicit)** — larger type → smaller type (`double` → `int`) — may lose precision, requires a cast operator `(int) d`.

Casts between reference types follow the class hierarchy and may throw `ClassCastException` at runtime if the object is not actually an instance of the target type.

**References:**
- [Java Language Spec — Conversions and Contexts](https://docs.oracle.com/javase/specs/jls/se17/html/jls-5.html)
- [Baeldung: Java Type Casting](https://www.baeldung.com/java-type-casting)

#### Java Loop Constructs

Java provides three core loop constructs:

• **`for` loop** — best when the number of iterations is known (`for (int i = 0; i < n; i++)`).
• **`while` loop** — evaluates the condition before each iteration; body may execute zero times.
• **`do-while` loop** — evaluates the condition *after* each iteration; body always executes at least once.

Java 5 added the **enhanced for-each** (`for (T item : collection)`) for iterating over arrays and `Iterable` types.

**References:**
- [Oracle Java Tutorials — The for Statement](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/for.html)
- [Baeldung: Loops in Java](https://www.baeldung.com/java-loops)

#### Java Operators & Operator Precedence

Java operators fall into several families:

• **Arithmetic** — `+ - * / %` (modulus)
• **Relational** — `== != > < >= <=`
• **Logical** — `&& || !`
• **Bitwise** — `& | ^ ~ << >>`
• **Ternary** — `condition ? a : b`
• **Assignment** — `= += -= *= /= %=`

**Precedence** determines evaluation order when an expression mixes operators (e.g., `*` before `+`). Parentheses override default precedence.

**References:**
- [Oracle Java Tutorials — Operators](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/operators.html)
- [Baeldung: Java Operators](https://www.baeldung.com/java-operators)

#### Java Constructors & Object Creation

A **constructor** is a special method invoked via `new ClassName(...)` to initialise a newly allocated object. If no constructor is defined, Java provides a default no-arg constructor. Constructors can be overloaded, and `this(...)` chains one constructor to another within the same class. In Spring, the container calls the constructor when creating a bean, injecting dependencies as constructor arguments.

**References:**
- [Oracle Java Tutorials — Constructors](https://docs.oracle.com/javase/tutorial/java/javaOO/constructors.html)
- [Baeldung: Java Constructors](https://www.baeldung.com/java-constructors)

#### Servlet Request Forwarding (RequestDispatcher)

`RequestDispatcher.forward(req, res)` transfers control from one servlet to another **entirely on the server side** — the browser URL does *not* change. The original request and response objects are shared, so data attached via `req.setAttribute()` is available to the target servlet. This is the preferred approach when you want to delegate processing without an extra HTTP round-trip.

**References:**
- [Jakarta Servlet — RequestDispatcher](https://jakarta.ee/specifications/servlet/6.0/)
- [Baeldung: Redirect vs Forward in Servlets](https://www.baeldung.com/servlet-redirect-forward)

#### HTTP Redirect & URL Rewriting

`res.sendRedirect(url)` sends an HTTP 302 response telling the browser to make a **new request** to a different URL. The browser address bar updates. Data can be passed by appending query parameters to the URL (URL rewriting), but this exposes values in the address bar. Redirects are useful after POST operations (Post-Redirect-Get pattern) to prevent duplicate form submissions.

**References:**
- [MDN: HTTP Redirections](https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections)
- [Baeldung: Redirect vs Forward in Servlets](https://www.baeldung.com/servlet-redirect-forward)

#### Java Access Modifiers

Access modifiers control visibility of classes, fields, and methods:

• **`public`** — accessible from everywhere.
• **`protected`** — accessible within the same package and subclasses.
• *default (package-private)* — accessible only within the same package.
• **`private`** — accessible only within the declaring class.

In interfaces, methods are `public` by default. Choosing the right modifier enforces encapsulation and limits the API surface.

**References:**
- [Oracle Java Tutorials — Controlling Access](https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html)
- [Baeldung: Java Access Modifiers](https://www.baeldung.com/java-access-modifiers)

#### Java `static` Keyword

The `static` modifier means the member belongs to the **class** rather than to any instance. Static fields are shared across all instances; static methods can be called without creating an object. `main(String[])` is static because the JVM needs an entry point before any object exists. A common pitfall: static methods cannot access instance fields or call instance methods directly.

**References:**
- [Oracle Java Tutorials — Class Variables](https://docs.oracle.com/javase/tutorial/java/javaOO/classvars.html)
- [Baeldung: The static Keyword in Java](https://www.baeldung.com/java-static)

#### Java `final` Keyword & Immutability

The `final` keyword prevents reassignment:

• **`final` variable** — value cannot be changed after initialisation; combined with constructor injection this ensures dependencies are immutable.
• **`final` method** — cannot be overridden by subclasses.
• **`final` class** — cannot be extended (`String` is `final`).

In Spring, constructor-injected fields are typically `final`, guaranteeing the dependency is never accidentally replaced.

**References:**
- [Oracle Java Tutorials — The final Keyword](https://docs.oracle.com/javase/tutorial/java/IandI/final.html)
- [Baeldung: The final Keyword in Java](https://www.baeldung.com/java-final)

#### Writing HTTP Responses with PrintWriter

`HttpServletResponse.getWriter()` returns a `PrintWriter` that streams character data back to the client's browser. Calling `out.println(...)` writes directly to the HTTP response body. In modern Spring MVC, `@ResponseBody` and `@RestController` abstract this away, but understanding the raw mechanism clarifies how controllers ultimately send data to the user.

**References:**
- [Jakarta Servlet — HttpServletResponse](https://jakarta.ee/specifications/servlet/6.0/)
- [Baeldung: Guide to PrintWriter](https://www.baeldung.com/java-printwriter)

#### Java Primitive Data Types

Java has eight primitive types:

• **Integers:** `byte` (8-bit), `short` (16-bit), `int` (32-bit), `long` (64-bit)
• **Floating-point:** `float` (32-bit), `double` (64-bit)
• **Character:** `char` (16-bit Unicode)
• **Boolean:** `boolean` (`true`/`false`)

Primitives are stored on the stack (or inlined) and are much faster than their wrapper counterparts. Literal suffixes like `f`, `L`, `d` disambiguate types.

**References:**
- [Oracle Java Tutorials — Primitive Data Types](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html)
- [Baeldung: Java Primitive Types](https://www.baeldung.com/java-primitives)

---

## Entry #2 — 2026-02-22 | Commit: `7e7b4e7` — Merge branch 'master' of https://github.com/shivam-jha2712/Spring-Boot-All

> **Author:** Shivam Jha

### Summary

No new concepts were introduced beyond those already documented in Entry #1.
