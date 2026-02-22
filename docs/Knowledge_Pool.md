# Knowledge Pool

This file is automatically maintained by the
[`update-knowledge-pool`](.github/workflows/update-knowledge-pool.yml)
GitHub Actions workflow.

Each entry is generated on every push to `master`, summarising the Spring Boot
and Java concepts introduced in that commit.

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

#### Spring Boot Externalised Configuration

Spring Boot supports externalised configuration via `application.properties` or `application.yml`. `@Value("${property.key}")` injects individual properties; `@ConfigurationProperties(prefix = "…")` binds a whole group of properties to a typed POJO, enabling IDE autocompletion and JSR-303 validation.

**References:**
- [Spring Boot — Common Application Properties](https://docs.spring.io/spring-boot/docs/current/reference/html/application-properties.html)
- [Baeldung: @ConfigurationProperties Guide](https://www.baeldung.com/configuration-properties-in-spring-boot)

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

---

## Entry #2 — 2026-02-22 | Commit: `7e7b4e7` — Merge branch 'master' of https://github.com/shivam-jha2712/Spring-Boot-All

> **Author:** Shivam Jha

### Summary

No new Spring Boot or Java framework patterns were introduced beyond those already documented in Entry #1.

