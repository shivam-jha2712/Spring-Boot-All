#!/usr/bin/env python3
"""Analyze the latest git commit and append a learning entry to docs/Knowledge_Pool.md.

The script scans two sources for every commit:
  1. The **added lines** from the unified diff (only lines starting with ``+``),
     so that only genuinely new content is considered — not pre-existing code.
  2. The commit message itself.

Patterns are matched against **two** registries:
  • CONCEPT_REGISTRY  — code-level patterns (annotations, class names, APIs).
  • GENERAL_CONCEPT_REGISTRY — comment-level / keyword patterns that detect
    shorthand notes, questions, and explanations the author writes in comments
    (e.g. "IOC?", "tight coupling", "auto-boxing").
"""

import subprocess
import re
import os
from datetime import datetime

DOCS_DIR = "docs"
KNOWLEDGE_POOL_FILE = os.path.join(DOCS_DIR, "Knowledge_Pool.md")

# ---------------------------------------------------------------------------
# Concept registry — CODE patterns (annotations, APIs, class names)
# Each tuple: (regex_pattern, concept_dict)
# concept_dict keys: name, explanation, image_key, links (list of (url, title))
# ---------------------------------------------------------------------------
CONCEPT_REGISTRY = [
    (
        r"@SpringBootApplication",
        {
            "name": "Spring Boot Auto-Configuration & Application Bootstrap",
            "explanation": (
                "`@SpringBootApplication` is a convenience meta-annotation that combines "
                "`@Configuration`, `@EnableAutoConfiguration`, and `@ComponentScan`. "
                "It marks the main class of a Spring Boot application, triggers classpath "
                "scanning for beans, and enables opinionated auto-configuration so that "
                "sensible infrastructure defaults are applied without any manual bean "
                "declarations."
            ),
            "image_key": "spring_boot_bootstrap",
            "links": [
                (
                    "https://docs.spring.io/spring-boot/docs/current/reference/html/using.html"
                    "#using.using-the-springbootapplication-annotation",
                    "Spring Boot Reference — @SpringBootApplication",
                ),
                (
                    "https://docs.spring.io/spring-boot/docs/current/reference/html/"
                    "auto-configuration-classes.html",
                    "Spring Boot Auto-Configuration Classes",
                ),
            ],
        },
    ),
    (
        r"@RestController",
        {
            "name": "Spring MVC REST Controller",
            "explanation": (
                "`@RestController` is a stereotype annotation that combines `@Controller` "
                "and `@ResponseBody`. Every method in a `@RestController` class automatically "
                "serialises its return value (typically to JSON via Jackson) and writes it "
                "directly to the HTTP response body, bypassing view resolution entirely."
            ),
            "image_key": "rest_controller",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/"
                    "springframework/web/bind/annotation/RestController.html",
                    "Spring API — @RestController",
                ),
                (
                    "https://spring.io/guides/gs/rest-service/",
                    "Spring Guide: Building a RESTful Web Service",
                ),
            ],
        },
    ),
    (
        r"@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)",
        {
            "name": "Spring MVC Request Mapping",
            "explanation": (
                "Request-mapping annotations (`@GetMapping`, `@PostMapping`, `@PutMapping`, "
                "`@DeleteMapping`, `@PatchMapping`) are composed shorthand forms of "
                "`@RequestMapping` pre-bound to a specific HTTP method. They map a handler "
                "method to a URL path and HTTP verb, enabling clean, RESTful endpoint "
                "declarations with minimal boilerplate."
            ),
            "image_key": "request_mapping",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "web.html#mvc-ann-requestmapping",
                    "Spring MVC Reference — Request Mapping",
                ),
                (
                    "https://www.baeldung.com/spring-requestmapping",
                    "Baeldung: Spring @RequestMapping Guide",
                ),
            ],
        },
    ),
    (
        r"@(Service|Component|Repository)\b",
        {
            "name": "Spring Stereotype Annotations & Bean Registration",
            "explanation": (
                "`@Service`, `@Component`, and `@Repository` mark classes as Spring-managed "
                "beans discovered automatically during component scanning. `@Repository` "
                "additionally enables persistence-exception translation, converting "
                "vendor-specific data-access exceptions into Spring's unified "
                "`DataAccessException` hierarchy."
            ),
            "image_key": "spring_stereotypes",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "core.html#beans-stereotype-annotations",
                    "Spring Core — Stereotype Annotations",
                ),
                (
                    "https://www.baeldung.com/spring-component-repository-service",
                    "Baeldung: @Component vs @Repository vs @Service",
                ),
            ],
        },
    ),
    (
        r"@(Entity|Table|Column|Id|GeneratedValue|OneToMany|ManyToOne|ManyToMany|OneToOne|JoinColumn)\b",
        {
            "name": "JPA / Hibernate Entity Mapping",
            "explanation": (
                "JPA annotations map Java classes to relational database tables. `@Entity` "
                "marks a POJO as a persistent entity; `@Table` and `@Column` customise "
                "table/column names. `@Id` defines the primary key and `@GeneratedValue` "
                "delegates key generation to the database or a sequence. Relationship "
                "annotations (`@OneToMany`, `@ManyToOne`, etc.) model foreign-key "
                "associations."
            ),
            "image_key": "jpa_entity_mapping",
            "links": [
                (
                    "https://jakarta.ee/specifications/persistence/3.1/"
                    "jakarta-persistence-spec-3.1.html",
                    "Jakarta Persistence 3.1 Specification",
                ),
                (
                    "https://www.baeldung.com/jpa-entities",
                    "Baeldung: JPA Entities",
                ),
                (
                    "https://docs.spring.io/spring-data/jpa/docs/current/reference/html/",
                    "Spring Data JPA Reference",
                ),
            ],
        },
    ),
    (
        r"(JpaRepository|CrudRepository|PagingAndSortingRepository)",
        {
            "name": "Spring Data JPA Repositories",
            "explanation": (
                "Spring Data JPA repositories eliminate boilerplate DAO code. Extending "
                "`JpaRepository<T, ID>` provides CRUD operations, pagination, and sorting "
                "out of the box — Spring generates the implementation at runtime via dynamic "
                "proxies. Derived query methods (e.g., `findByEmail`) are automatically "
                "translated into JPQL without writing any SQL."
            ),
            "image_key": "spring_data_jpa",
            "links": [
                (
                    "https://docs.spring.io/spring-data/jpa/docs/current/reference/html/"
                    "#repositories",
                    "Spring Data JPA Reference — Repositories",
                ),
                (
                    "https://www.baeldung.com/spring-data-repositories",
                    "Baeldung: Spring Data Repositories",
                ),
            ],
        },
    ),
    (
        r"@Transactional\b",
        {
            "name": "Spring Declarative Transaction Management",
            "explanation": (
                "`@Transactional` enables declarative transaction demarcation via AOP "
                "proxies. Spring wraps the annotated method: if it completes normally the "
                "transaction is committed; if an unchecked exception propagates it is rolled "
                "back. Attributes such as `propagation`, `isolation`, `timeout`, and "
                "`readOnly` provide fine-grained control."
            ),
            "image_key": "spring_transactional",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "data-access.html#transaction",
                    "Spring Reference — Transaction Management",
                ),
                (
                    "https://www.baeldung.com/transaction-configuration-with-jpa-and-spring",
                    "Baeldung: Transactions with JPA and Spring",
                ),
            ],
        },
    ),
    (
        r"(JWT|JwtUtil|JwtService|JwtFilter|jjwt)",
        {
            "name": "JSON Web Tokens (JWT) for Stateless Authentication",
            "explanation": (
                "JWTs are compact, URL-safe tokens made up of a Base64-encoded header, "
                "payload (claims), and HMAC/RSA signature. In Spring Security they are "
                "typically issued on login and validated inside a `OncePerRequestFilter`. "
                "Because the token encodes the user's identity and roles, the server stays "
                "completely stateless — no session store is required."
            ),
            "image_key": "jwt_authentication",
            "links": [
                (
                    "https://jwt.io/introduction/",
                    "JWT.io — Introduction to JSON Web Tokens",
                ),
                (
                    "https://www.baeldung.com/spring-security-oauth-jwt",
                    "Baeldung: Spring Security with JWT",
                ),
                (
                    "https://github.com/jwtk/jjwt",
                    "JJWT Library on GitHub",
                ),
            ],
        },
    ),
    (
        r"(BCrypt|PasswordEncoder|BCryptPasswordEncoder)",
        {
            "name": "Password Hashing with BCrypt",
            "explanation": (
                "BCrypt is an adaptive, salted password-hashing function. Each hash "
                "embeds a random salt, preventing rainbow-table attacks. "
                "`BCryptPasswordEncoder` in Spring Security applies BCrypt with a "
                "configurable work factor (cost), making brute-force attacks increasingly "
                "expensive as hardware improves."
            ),
            "image_key": "bcrypt_hashing",
            "links": [
                (
                    "https://docs.spring.io/spring-security/reference/features/"
                    "authentication/password-storage.html",
                    "Spring Security — Password Storage",
                ),
                (
                    "https://www.baeldung.com/spring-security-registration-password-"
                    "encoding-bcrypt",
                    "Baeldung: BCrypt Password Encoding",
                ),
            ],
        },
    ),
    (
        r"(SecurityFilterChain|HttpSecurity|@EnableWebSecurity)",
        {
            "name": "Spring Security Filter Chain Configuration",
            "explanation": (
                "`SecurityFilterChain` defines the HTTP security rules: which URLs require "
                "authentication, which roles grant access, and which authentication "
                "mechanism is in use (form login, JWT, OAuth2). `HttpSecurity` provides a "
                "fluent DSL to configure CSRF protection, CORS, session management, and "
                "exception handling."
            ),
            "image_key": "spring_security_filter_chain",
            "links": [
                (
                    "https://docs.spring.io/spring-security/reference/servlet/"
                    "configuration/java.html",
                    "Spring Security — Java Configuration",
                ),
                (
                    "https://www.baeldung.com/spring-security-basic-authentication",
                    "Baeldung: Spring Security Basic Auth",
                ),
            ],
        },
    ),
    (
        r"(RedisTemplate|@Cacheable|@CacheEvict|@EnableCaching|RedisConnectionFactory)",
        {
            "name": "Redis Caching with Spring",
            "explanation": (
                "Spring's caching abstraction (`@Cacheable`, `@CacheEvict`) decouples "
                "caching logic from business code. When backed by Redis via `RedisTemplate`, "
                "results are stored in Redis with an optional TTL. This dramatically reduces "
                "database load for frequently read, rarely changed data."
            ),
            "image_key": "redis_caching",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "integration.html#cache",
                    "Spring Reference — Cache Abstraction",
                ),
                (
                    "https://www.baeldung.com/spring-boot-redis-cache",
                    "Baeldung: Spring Boot with Redis Cache",
                ),
                (
                    "https://redis.io/docs/latest/develop/use/client-libraries/",
                    "Redis — Client Libraries Documentation",
                ),
            ],
        },
    ),
    (
        r"(@EnableWebSocketMessageBroker|WebSocketMessageBrokerConfigurer"
        r"|SimpMessagingTemplate|@MessageMapping)",
        {
            "name": "Spring WebSocket & STOMP Messaging",
            "explanation": (
                "`@EnableWebSocketMessageBroker` enables a full STOMP-over-WebSocket "
                "message broker. Clients subscribe to topics; the server broadcasts messages "
                "via `SimpMessagingTemplate`. `@MessageMapping` mirrors `@RequestMapping` "
                "for WebSocket message handlers, enabling real-time bidirectional "
                "communication without polling."
            ),
            "image_key": "spring_websocket",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "web.html#websocket",
                    "Spring Reference — WebSocket",
                ),
                (
                    "https://spring.io/guides/gs/messaging-stomp-websocket/",
                    "Spring Guide: STOMP over WebSocket",
                ),
            ],
        },
    ),
    (
        r"(@SpringBootTest|@WebMvcTest|@DataJpaTest|MockMvc|@MockBean)",
        {
            "name": "Spring Boot Testing Slices",
            "explanation": (
                "Spring Boot's test slices load only a relevant portion of the application "
                "context to keep tests fast. `@SpringBootTest` loads the full context; "
                "`@WebMvcTest` loads only the web layer; `@DataJpaTest` loads only JPA "
                "components. `MockMvc` enables controller testing without a running server, "
                "and `@MockBean` replaces a real bean with a Mockito mock."
            ),
            "image_key": "spring_boot_testing",
            "links": [
                (
                    "https://docs.spring.io/spring-boot/docs/current/reference/html/"
                    "test-auto-configuration.html",
                    "Spring Boot Test Auto-Configuration",
                ),
                (
                    "https://www.baeldung.com/spring-boot-testing",
                    "Baeldung: Testing in Spring Boot",
                ),
            ],
        },
    ),
    (
        r"@(Configuration|Bean)\b",
        {
            "name": "Spring Java-based Bean Configuration",
            "explanation": (
                "`@Configuration` marks a class as a source of bean definitions. Methods "
                "annotated with `@Bean` return objects that are registered as Spring-managed "
                "beans. This Java config approach is type-safe and refactor-friendly, "
                "replacing verbose XML-based Spring configuration."
            ),
            "image_key": "spring_configuration",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "core.html#beans-java",
                    "Spring Core — Java-based Configuration",
                ),
                (
                    "https://www.baeldung.com/spring-bean",
                    "Baeldung: Spring @Bean Annotation",
                ),
            ],
        },
    ),
    (
        r"(@Autowired|@Inject|Dependency Injection|Constructor.*Injection)\b",
        {
            "name": "Spring Dependency Injection",
            "explanation": (
                "Spring resolves and injects dependencies automatically. `@Autowired` "
                "injects by type; constructor injection (the recommended approach) makes "
                "dependencies explicit and allows fields to be `final`, improving "
                "testability and preventing null-injection bugs."
            ),
            "image_key": "spring_dependency_injection",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "core.html#beans-dependency-injection",
                    "Spring Core — Dependency Injection",
                ),
                (
                    "https://www.baeldung.com/constructor-injection-in-spring",
                    "Baeldung: Constructor Injection in Spring",
                ),
            ],
        },
    ),
    (
        r"(@CrossOrigin|CorsConfigurationSource|CorsConfiguration)\b",
        {
            "name": "CORS Configuration in Spring",
            "explanation": (
                "Cross-Origin Resource Sharing (CORS) controls which external domains may "
                "make HTTP requests to your API. `@CrossOrigin` on a controller or method "
                "allows fine-grained control. A global `CorsConfigurationSource` bean "
                "configures allowed origins, methods, and headers across the entire "
                "application."
            ),
            "image_key": "cors_configuration",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "web.html#mvc-cors",
                    "Spring MVC — CORS",
                ),
                (
                    "https://www.baeldung.com/spring-cors",
                    "Baeldung: CORS with Spring MVC",
                ),
            ],
        },
    ),
    (
        r"(Pageable|@PageableDefault|PageRequest|Page<)",
        {
            "name": "Pagination with Spring Data",
            "explanation": (
                "Spring Data's `Pageable` interface abstracts pagination and sorting. "
                "Repository methods that accept a `Pageable` parameter return a `Page<T>` "
                "containing the requested slice of results plus metadata (total pages, "
                "total elements). `PageRequest.of(page, size)` creates concrete `Pageable` "
                "instances."
            ),
            "image_key": "spring_pagination",
            "links": [
                (
                    "https://docs.spring.io/spring-data/commons/docs/current/api/org/"
                    "springframework/data/domain/Pageable.html",
                    "Spring Data — Pageable API",
                ),
                (
                    "https://www.baeldung.com/spring-data-jpa-pagination-sorting",
                    "Baeldung: Pagination and Sorting with Spring Data JPA",
                ),
            ],
        },
    ),
    (
        r"(@RequestBody|@PathVariable|@RequestParam|@ResponseBody)\b",
        {
            "name": "Spring MVC Method Argument Binding",
            "explanation": (
                "Spring MVC automatically binds HTTP request data to handler method "
                "parameters. `@RequestBody` deserialises the request body (JSON → Java); "
                "`@PathVariable` extracts URI template variables; `@RequestParam` binds "
                "query-string or form parameters; `@ResponseBody` serialises the return "
                "value to the response body."
            ),
            "image_key": "mvc_argument_binding",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "web.html#mvc-ann-methods",
                    "Spring MVC — Annotated Controller Methods",
                ),
                (
                    "https://www.baeldung.com/spring-request-response-body",
                    "Baeldung: @RequestBody and @ResponseBody",
                ),
            ],
        },
    ),
    (
        r"(application\.properties|application\.yml|@Value\(|@ConfigurationProperties)",
        {
            "name": "Spring Boot Externalised Configuration",
            "explanation": (
                "Spring Boot supports externalised configuration via `application.properties` "
                "or `application.yml`. `@Value(\"${property.key}\")` injects individual "
                "properties; `@ConfigurationProperties(prefix = \"…\")` binds a whole group "
                "of properties to a typed POJO, enabling IDE autocompletion and "
                "JSR-303 validation."
            ),
            "image_key": "spring_boot_config",
            "links": [
                (
                    "https://docs.spring.io/spring-boot/docs/current/reference/html/"
                    "application-properties.html",
                    "Spring Boot — Common Application Properties",
                ),
                (
                    "https://www.baeldung.com/configuration-properties-in-spring-boot",
                    "Baeldung: @ConfigurationProperties Guide",
                ),
            ],
        },
    ),
    (
        r"(ResponseEntity|HttpStatus)\b",
        {
            "name": "Spring MVC ResponseEntity & HTTP Status Codes",
            "explanation": (
                "`ResponseEntity<T>` gives full control over the HTTP response: status code, "
                "headers, and body. Using it instead of a plain return type lets controllers "
                "communicate meaningful HTTP semantics (201 Created, 404 Not Found, etc.) "
                "to REST clients, improving API clarity."
            ),
            "image_key": "response_entity",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/"
                    "springframework/http/ResponseEntity.html",
                    "Spring API — ResponseEntity",
                ),
                (
                    "https://www.baeldung.com/spring-response-entity",
                    "Baeldung: Using Spring ResponseEntity",
                ),
            ],
        },
    ),
    (
        r"(@ExceptionHandler|@ControllerAdvice|@RestControllerAdvice)",
        {
            "name": "Spring Global Exception Handling",
            "explanation": (
                "`@ControllerAdvice` (or `@RestControllerAdvice`) defines cross-cutting "
                "exception handlers. Methods annotated with `@ExceptionHandler` intercept "
                "specific exception types thrown by any controller, centralising "
                "error-response logic and eliminating duplicated try/catch blocks."
            ),
            "image_key": "spring_exception_handling",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "web.html#mvc-ann-exceptionhandler",
                    "Spring MVC — @ExceptionHandler",
                ),
                (
                    "https://www.baeldung.com/exception-handling-for-rest-with-spring",
                    "Baeldung: REST Error Handling with Spring",
                ),
            ],
        },
    ),
    (
        r"(@ConditionalOnProperty|@ConditionalOnBean|@ConditionalOnMissingBean|@ConditionalOnClass)",
        {
            "name": "Spring Boot Conditional Bean Configuration",
            "explanation": (
                "Spring Boot conditional annotations control whether a bean is registered "
                "based on runtime conditions. `@ConditionalOnProperty` activates a bean "
                "only when a specific property matches a given value — ideal for switching "
                "between implementations (e.g., payment providers) via `application.properties`. "
                "`@ConditionalOnBean` and `@ConditionalOnMissingBean` check for the "
                "presence or absence of other beans in the context."
            ),
            "image_key": "conditional_bean_config",
            "links": [
                (
                    "https://docs.spring.io/spring-boot/docs/current/reference/html/"
                    "features.html#features.developing-auto-configuration.condition-annotations",
                    "Spring Boot — Condition Annotations",
                ),
                (
                    "https://www.baeldung.com/spring-conditionalonproperty",
                    "Baeldung: @ConditionalOnProperty Guide",
                ),
            ],
        },
    ),
    (
        r"(CommandLineRunner|ApplicationRunner)",
        {
            "name": "Spring Boot Application Startup Runners",
            "explanation": (
                "`CommandLineRunner` and `ApplicationRunner` are functional interfaces "
                "whose `run` method is invoked once the `ApplicationContext` is fully "
                "initialised. They are used to execute one-time startup logic — such as "
                "seeding a database, warming a cache, or verifying external services — "
                "without resorting to `@PostConstruct` or static initialiser blocks."
            ),
            "image_key": "command_line_runner",
            "links": [
                (
                    "https://docs.spring.io/spring-boot/docs/current/reference/html/"
                    "features.html#features.spring-application.command-line-runner",
                    "Spring Boot Reference — CommandLineRunner",
                ),
                (
                    "https://www.baeldung.com/running-setup-logic-on-startup-in-spring",
                    "Baeldung: Running Logic on Startup in Spring",
                ),
            ],
        },
    ),
    (
        r"(HttpServlet|@WebServlet|HttpServletRequest|HttpServletResponse|RequestDispatcher)",
        {
            "name": "Java Servlet Fundamentals",
            "explanation": (
                "Java Servlets are the foundation of server-side web development in Java. "
                "`HttpServlet` processes HTTP requests via `doGet`/`doPost` methods. "
                "`HttpServletRequest` and `HttpServletResponse` provide access to request "
                "parameters, headers, cookies, and sessions. `RequestDispatcher` enables "
                "server-side forwarding between servlets. Understanding servlets is key to "
                "appreciating what Spring MVC abstracts away."
            ),
            "image_key": "java_servlets",
            "links": [
                (
                    "https://jakarta.ee/specifications/servlet/6.0/",
                    "Jakarta Servlet 6.0 Specification",
                ),
                (
                    "https://www.baeldung.com/intro-to-servlets",
                    "Baeldung: Introduction to Java Servlets",
                ),
            ],
        },
    ),
    (
        r"(HttpSession|Cookie\b|req\.getCookies|res\.addCookie|session\.setAttribute|session\.getAttribute)",
        {
            "name": "Servlet Session Management & Cookies",
            "explanation": (
                "HTTP is stateless; `HttpSession` and `Cookie` are the two primary "
                "mechanisms for maintaining state across requests. `HttpSession` stores "
                "data server-side and tracks users via a `JSESSIONID` cookie. Cookies "
                "store small key-value pairs on the client browser. Understanding these "
                "primitives is essential before adopting Spring Session or Spring Security's "
                "session management."
            ),
            "image_key": "servlet_sessions_cookies",
            "links": [
                (
                    "https://jakarta.ee/specifications/servlet/6.0/",
                    "Jakarta Servlet Specification — Sessions",
                ),
                (
                    "https://www.baeldung.com/java-servlet-cookies-session",
                    "Baeldung: Cookies and Session in Servlets",
                ),
            ],
        },
    ),
    (
        r"(?i)(Inversion.of.Control|\bIoC\b|\bimplements\b.*Service)",
        {
            "name": "Inversion of Control (IoC) & Interface-based Design",
            "explanation": (
                "Inversion of Control is the core principle behind Spring's DI container. "
                "Instead of a class creating its own dependencies, the framework injects "
                "them. Programming to interfaces (e.g., a `PaymentService` interface with "
                "multiple implementations) enables loose coupling: the consuming class "
                "depends only on the contract, and the concrete implementation is selected "
                "at runtime by the Spring container."
            ),
            "image_key": "ioc_interfaces",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "core.html#beans-introduction",
                    "Spring Core — IoC Container Introduction",
                ),
                (
                    "https://www.baeldung.com/inversion-control-and-dependency-injection-in-spring",
                    "Baeldung: IoC and DI in Spring",
                ),
            ],
        },
    ),
]

# ---------------------------------------------------------------------------
# General concept registry — COMMENT / KEYWORD patterns
#
# These patterns are intentionally broad and case-insensitive.  They match
# shorthand notes, questions, and explanations that developers write in code
# comments (e.g. "IOC?", "tight coupling", "auto-boxing", "OOP", "extends").
# ---------------------------------------------------------------------------
GENERAL_CONCEPT_REGISTRY = [
    # ── OOP Fundamentals ────────────────────────────────────────────────
    (
        r"(?i)\b(OOP|object.oriented|encapsulat|abstraction|polymorphism)\b",
        {
            "name": "Object-Oriented Programming (OOP) Principles",
            "explanation": (
                "OOP organises code around **objects** — instances of classes that bundle "
                "state (fields) and behaviour (methods). The four pillars are:\n\n"
                "• **Encapsulation** — hiding internal state behind access modifiers and "
                "exposing behaviour through public methods.\n"
                "• **Abstraction** — modelling real-world entities at the right level of "
                "detail, exposing only what matters to the caller.\n"
                "• **Inheritance** — sharing behaviour via parent–child class hierarchies "
                "(`extends`).\n"
                "• **Polymorphism** — one interface, many implementations; a reference "
                "of the parent type can point to any child object, and the correct "
                "method is resolved at runtime (dynamic dispatch)."
            ),
            "image_key": "oop_principles",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/concepts/",
                    "Oracle Java Tutorials — OOP Concepts",
                ),
                (
                    "https://www.baeldung.com/java-oop",
                    "Baeldung: OOP Concepts in Java",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(inherit|extends\b|super\b|parent.class|child.class)\b",
        {
            "name": "Java Inheritance & the `extends` Keyword",
            "explanation": (
                "Inheritance lets a **child class** (`extends`) reuse and specialise the "
                "fields and methods of a **parent class**. The child inherits all "
                "non-private members and can override methods to provide its own "
                "implementation. `super` refers to the parent instance — used to call "
                "the parent constructor or an overridden method. Java supports single "
                "class inheritance but multiple interface implementation."
            ),
            "image_key": "java_inheritance",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html",
                    "Oracle Java Tutorials — Inheritance",
                ),
                (
                    "https://www.baeldung.com/java-inheritance",
                    "Baeldung: Guide to Inheritance in Java",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(interface\b|implements\b|abstract\s+(class|method)|default\s+method)",
        {
            "name": "Java Interfaces & Abstract Classes",
            "explanation": (
                "An **interface** defines a contract — method signatures without "
                "implementation (plus `default` methods since Java 8). A class "
                "`implements` one or more interfaces, promising to provide the method "
                "bodies. An **abstract class** sits between a concrete class and an "
                "interface: it can hold state and concrete methods but cannot be "
                "instantiated. Use interfaces for capability contracts and abstract "
                "classes for shared base behaviour."
            ),
            "image_key": "interfaces_abstract",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/IandI/createinterface.html",
                    "Oracle Java Tutorials — Interfaces",
                ),
                (
                    "https://www.baeldung.com/java-interface-vs-abstract-class",
                    "Baeldung: Interface vs Abstract Class",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(@Override|method.overrid|overrid)",
        {
            "name": "Method Overriding in Java",
            "explanation": (
                "When a subclass provides its own version of a method already defined in "
                "its parent, it **overrides** that method. The `@Override` annotation is "
                "optional but strongly recommended — the compiler will flag an error if the "
                "annotated method does not actually override a superclass method, catching "
                "typos and signature mismatches early. At runtime, the JVM uses dynamic "
                "dispatch to call the overridden version."
            ),
            "image_key": "method_overriding",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/IandI/override.html",
                    "Oracle Java Tutorials — Overriding Methods",
                ),
                (
                    "https://www.baeldung.com/java-method-overriding",
                    "Baeldung: Method Overriding in Java",
                ),
            ],
        },
    ),
    # ── Coupling & Design ───────────────────────────────────────────────
    (
        r"(?i)\b(tight.coupling|loose.coupling|loosely.coupled|tightly.coupled|decoupl)\b",
        {
            "name": "Tight vs Loose Coupling",
            "explanation": (
                "**Tight coupling** means a class directly creates or depends on a concrete "
                "implementation (e.g., `new RazorpayPaymentService()`). Changing the "
                "dependency forces changes in the consumer. **Loose coupling** means the "
                "consumer depends on an *abstraction* (interface), and the concrete "
                "implementation is supplied externally — typically via dependency injection. "
                "Loose coupling improves testability, swappability, and maintainability."
            ),
            "image_key": "coupling",
            "links": [
                (
                    "https://www.baeldung.com/java-coupling-classes-tight-loose",
                    "Baeldung: Tight and Loose Coupling in Java",
                ),
                (
                    "https://en.wikipedia.org/wiki/Coupling_(computer_programming)",
                    "Wikipedia: Coupling (Computer Programming)",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(strategy.pattern|switch.*implementation|swap.*implementation|multiple.implementation)",
        {
            "name": "Strategy Design Pattern",
            "explanation": (
                "The Strategy pattern defines a family of interchangeable algorithms "
                "behind a common interface. The client depends only on the interface; the "
                "concrete strategy is selected at configuration or runtime. In Spring this "
                "maps naturally to an interface with multiple `@Component` implementations, "
                "selected via `@ConditionalOnProperty`, `@Qualifier`, or profiles."
            ),
            "image_key": "strategy_pattern",
            "links": [
                (
                    "https://refactoring.guru/design-patterns/strategy",
                    "Refactoring Guru: Strategy Pattern",
                ),
                (
                    "https://www.baeldung.com/java-strategy-pattern",
                    "Baeldung: Strategy Pattern in Java",
                ),
            ],
        },
    ),
    # ── Spring / DI keywords in comments ────────────────────────────────
    (
        r"(?i)\bIOC\b|\binversion.of.control\b",
        {
            "name": "Inversion of Control (IoC)",
            "explanation": (
                "**IoC** flips the traditional flow of control: instead of *your* code "
                "creating dependencies, a **container** (the Spring `ApplicationContext`) "
                "creates them and *injects* them into your objects. This is the foundational "
                "principle behind Spring's dependency injection. Your classes declare "
                "*what* they need (via constructor parameters, `@Autowired`, or "
                "`@Inject`); the container decides *how* and *when* to fulfil those needs."
            ),
            "image_key": "ioc",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "core.html#beans-introduction",
                    "Spring Core — IoC Container",
                ),
                (
                    "https://martinfowler.com/bliki/InversionOfControl.html",
                    "Martin Fowler: Inversion of Control",
                ),
                (
                    "https://www.baeldung.com/inversion-control-and-dependency-injection-in-spring",
                    "Baeldung: IoC and DI in Spring",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(bean\b|spring.bean|bean.class|creation.of.bean|bean.*instantiat)",
        {
            "name": "Spring Beans & the Bean Lifecycle",
            "explanation": (
                "A **bean** is any object managed by the Spring IoC container. Beans are "
                "created (instantiated), configured (dependencies injected), initialised "
                "(`@PostConstruct`), and eventually destroyed (`@PreDestroy`). By default "
                "beans are **singletons** — one instance per application context. Marking a "
                "class with `@Component`, `@Service`, `@Repository`, or defining it in a "
                "`@Configuration` class registers it as a bean."
            ),
            "image_key": "spring_beans",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "core.html#beans-definition",
                    "Spring Core — Bean Overview",
                ),
                (
                    "https://www.baeldung.com/spring-bean",
                    "Baeldung: What is a Spring Bean?",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(component.scan|class.?path.scan|auto.?detect)",
        {
            "name": "Spring Component Scanning",
            "explanation": (
                "Component scanning is the mechanism by which Spring automatically "
                "discovers classes annotated with `@Component` (and its stereotypes "
                "`@Service`, `@Repository`, `@Controller`) on the classpath and registers "
                "them as beans. `@SpringBootApplication` implicitly enables scanning from "
                "the package it lives in downward, so any annotated class in a sub-package "
                "is automatically picked up."
            ),
            "image_key": "component_scanning",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "core.html#beans-classpath-scanning",
                    "Spring Core — Classpath Scanning",
                ),
                (
                    "https://www.baeldung.com/spring-component-scanning",
                    "Baeldung: Spring Component Scanning",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(field.injection|constructor.injection|setter.injection|constructor.DI|field.DI)\b",
        {
            "name": "Dependency Injection Styles: Constructor vs Field vs Setter",
            "explanation": (
                "Spring supports three injection styles:\n\n"
                "• **Constructor injection** (recommended) — dependencies are passed via "
                "the constructor; fields can be `final`, making the object immutable and "
                "easy to test.\n"
                "• **Setter injection** — dependencies are set via public setter methods "
                "after construction.\n"
                "• **Field injection** (`@Autowired` on a field) — convenient but "
                "prevents `final` fields, hides dependencies from the public API, and "
                "makes unit testing harder without a DI container.\n\n"
                "The Spring team officially recommends constructor injection."
            ),
            "image_key": "di_styles",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "core.html#beans-setter-injection",
                    "Spring Core — Setter-based DI",
                ),
                (
                    "https://www.baeldung.com/constructor-injection-in-spring",
                    "Baeldung: Constructor Injection in Spring",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(application.?context|ApplicationContext)\b",
        {
            "name": "Spring ApplicationContext",
            "explanation": (
                "The `ApplicationContext` is the central interface of the Spring IoC "
                "container. It loads bean definitions, wires dependencies, manages the "
                "bean lifecycle, and publishes application events. "
                "`SpringApplication.run(...)` in a Spring Boot app creates and refreshes "
                "an `ApplicationContext`, making all declared beans available for injection."
            ),
            "image_key": "application_context",
            "links": [
                (
                    "https://docs.spring.io/spring-framework/docs/current/reference/html/"
                    "core.html#context-introduction",
                    "Spring Core — ApplicationContext",
                ),
                (
                    "https://www.baeldung.com/spring-application-context",
                    "Baeldung: ApplicationContext in Spring",
                ),
            ],
        },
    ),
    # ── Java fundamentals (operators, casting, strings, loops) ──────────
    (
        r"(?i)\b(auto.?box|unbox|wrapper.class)\b|Integer\.valueOf|\.intValue\(\)",
        {
            "name": "Java Auto-boxing & Unboxing",
            "explanation": (
                "Auto-boxing is the automatic conversion from a primitive (`int`, "
                "`double`, `boolean`) to its wrapper class (`Integer`, `Double`, "
                "`Boolean`). Unboxing is the reverse. The compiler inserts `valueOf()` / "
                "`intValue()` calls behind the scenes. While convenient, excessive "
                "auto-boxing in hot loops can cause unnecessary object creation and GC "
                "pressure."
            ),
            "image_key": "autoboxing",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/data/autoboxing.html",
                    "Oracle Java Tutorials — Autoboxing and Unboxing",
                ),
                (
                    "https://www.baeldung.com/java-wrapper-classes",
                    "Baeldung: Java Wrapper Classes",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(type.?cast|explicit.cast|narrow.conver|widen.conver)\b|\([a-z]+\)\s*\w",
        {
            "name": "Java Type Casting",
            "explanation": (
                "Java supports two kinds of type conversion:\n\n"
                "• **Widening (implicit)** — smaller type → larger type (`int` → `double`) "
                "— no data loss, done automatically.\n"
                "• **Narrowing (explicit)** — larger type → smaller type (`double` → `int`) "
                "— may lose precision, requires a cast operator `(int) d`.\n\n"
                "Casts between reference types follow the class hierarchy and may throw "
                "`ClassCastException` at runtime if the object is not actually an instance "
                "of the target type."
            ),
            "image_key": "type_casting",
            "links": [
                (
                    "https://docs.oracle.com/javase/specs/jls/se17/html/jls-5.html",
                    "Java Language Spec — Conversions and Contexts",
                ),
                (
                    "https://www.baeldung.com/java-type-casting",
                    "Baeldung: Java Type Casting",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(for.loop|while.loop|do.while|loop.iteration)\b|\bfor\s*\(|\bwhile\s*\(|\bdo\s*\{",
        {
            "name": "Java Loop Constructs",
            "explanation": (
                "Java provides three core loop constructs:\n\n"
                "• **`for` loop** — best when the number of iterations is known "
                "(`for (int i = 0; i < n; i++)`).\n"
                "• **`while` loop** — evaluates the condition before each iteration; "
                "body may execute zero times.\n"
                "• **`do-while` loop** — evaluates the condition *after* each iteration; "
                "body always executes at least once.\n\n"
                "Java 5 added the **enhanced for-each** (`for (T item : collection)`) "
                "for iterating over arrays and `Iterable` types."
            ),
            "image_key": "java_loops",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/for.html",
                    "Oracle Java Tutorials — The for Statement",
                ),
                (
                    "https://www.baeldung.com/java-loops",
                    "Baeldung: Loops in Java",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(operator|arithmetic|relational|logical|bitwise|ternary|modulus|precedence)\b",
        {
            "name": "Java Operators & Operator Precedence",
            "explanation": (
                "Java operators fall into several families:\n\n"
                "• **Arithmetic** — `+ - * / %` (modulus)\n"
                "• **Relational** — `== != > < >= <=`\n"
                "• **Logical** — `&& || !`\n"
                "• **Bitwise** — `& | ^ ~ << >>`\n"
                "• **Ternary** — `condition ? a : b`\n"
                "• **Assignment** — `= += -= *= /= %=`\n\n"
                "**Precedence** determines evaluation order when an expression mixes "
                "operators (e.g., `*` before `+`). Parentheses override default precedence."
            ),
            "image_key": "java_operators",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/operators.html",
                    "Oracle Java Tutorials — Operators",
                ),
                (
                    "https://www.baeldung.com/java-operators",
                    "Baeldung: Java Operators",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(constructor\b|this\s*\(|object.creation|instantiat)\b|new\s+[\w.]+\s*\(",
        {
            "name": "Java Constructors & Object Creation",
            "explanation": (
                "A **constructor** is a special method invoked via `new ClassName(...)` to "
                "initialise a newly allocated object. If no constructor is defined, Java "
                "provides a default no-arg constructor. Constructors can be overloaded, and "
                "`this(...)` chains one constructor to another within the same class. "
                "In Spring, the container calls the constructor when creating a bean, "
                "injecting dependencies as constructor arguments."
            ),
            "image_key": "java_constructors",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/javaOO/constructors.html",
                    "Oracle Java Tutorials — Constructors",
                ),
                (
                    "https://www.baeldung.com/java-constructors",
                    "Baeldung: Java Constructors",
                ),
            ],
        },
    ),
    # ── Web / Servlet concepts from comments ────────────────────────────
    (
        r"(?i)\b(request.?dispatch|forward|server.side.forward)\b",
        {
            "name": "Servlet Request Forwarding (RequestDispatcher)",
            "explanation": (
                "`RequestDispatcher.forward(req, res)` transfers control from one servlet "
                "to another **entirely on the server side** — the browser URL does *not* "
                "change. The original request and response objects are shared, so data "
                "attached via `req.setAttribute()` is available to the target servlet. "
                "This is the preferred approach when you want to delegate processing "
                "without an extra HTTP round-trip."
            ),
            "image_key": "request_forwarding",
            "links": [
                (
                    "https://jakarta.ee/specifications/servlet/6.0/",
                    "Jakarta Servlet — RequestDispatcher",
                ),
                (
                    "https://www.baeldung.com/servlet-redirect-forward",
                    "Baeldung: Redirect vs Forward in Servlets",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(sendRedirect|URL.?rewrit|redirect.*client|client.side.redirect)\b",
        {
            "name": "HTTP Redirect & URL Rewriting",
            "explanation": (
                "`res.sendRedirect(url)` sends an HTTP 302 response telling the browser "
                "to make a **new request** to a different URL. The browser address bar "
                "updates. Data can be passed by appending query parameters to the URL "
                "(URL rewriting), but this exposes values in the address bar. Redirects "
                "are useful after POST operations (Post-Redirect-Get pattern) to prevent "
                "duplicate form submissions."
            ),
            "image_key": "http_redirect",
            "links": [
                (
                    "https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections",
                    "MDN: HTTP Redirections",
                ),
                (
                    "https://www.baeldung.com/servlet-redirect-forward",
                    "Baeldung: Redirect vs Forward in Servlets",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(access.modif|public\b|private\b|protected\b|default.access)",
        {
            "name": "Java Access Modifiers",
            "explanation": (
                "Access modifiers control visibility of classes, fields, and methods:\n\n"
                "• **`public`** — accessible from everywhere.\n"
                "• **`protected`** — accessible within the same package and subclasses.\n"
                "• *default (package-private)* — accessible only within the same package.\n"
                "• **`private`** — accessible only within the declaring class.\n\n"
                "In interfaces, methods are `public` by default. Choosing the right "
                "modifier enforces encapsulation and limits the API surface."
            ),
            "image_key": "access_modifiers",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html",
                    "Oracle Java Tutorials — Controlling Access",
                ),
                (
                    "https://www.baeldung.com/java-access-modifiers",
                    "Baeldung: Java Access Modifiers",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(static\b|static.method|static.field|class.level)",
        {
            "name": "Java `static` Keyword",
            "explanation": (
                "The `static` modifier means the member belongs to the **class** rather "
                "than to any instance. Static fields are shared across all instances; "
                "static methods can be called without creating an object. `main(String[])` "
                "is static because the JVM needs an entry point before any object exists. "
                "A common pitfall: static methods cannot access instance fields or call "
                "instance methods directly."
            ),
            "image_key": "java_static",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/javaOO/classvars.html",
                    "Oracle Java Tutorials — Class Variables",
                ),
                (
                    "https://www.baeldung.com/java-static",
                    "Baeldung: The static Keyword in Java",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(final\b|immutable|cannot.be.changed|constant)\b",
        {
            "name": "Java `final` Keyword & Immutability",
            "explanation": (
                "The `final` keyword prevents reassignment:\n\n"
                "• **`final` variable** — value cannot be changed after initialisation; "
                "combined with constructor injection this ensures dependencies are immutable.\n"
                "• **`final` method** — cannot be overridden by subclasses.\n"
                "• **`final` class** — cannot be extended (`String` is `final`).\n\n"
                "In Spring, constructor-injected fields are typically `final`, "
                "guaranteeing the dependency is never accidentally replaced."
            ),
            "image_key": "java_final",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/IandI/final.html",
                    "Oracle Java Tutorials — The final Keyword",
                ),
                (
                    "https://www.baeldung.com/java-final",
                    "Baeldung: The final Keyword in Java",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(PrintWriter|getWriter|response.body|write.*browser|output.*client)",
        {
            "name": "Writing HTTP Responses with PrintWriter",
            "explanation": (
                "`HttpServletResponse.getWriter()` returns a `PrintWriter` that streams "
                "character data back to the client's browser. Calling `out.println(...)` "
                "writes directly to the HTTP response body. In modern Spring MVC, "
                "`@ResponseBody` and `@RestController` abstract this away, but "
                "understanding the raw mechanism clarifies how controllers ultimately "
                "send data to the user."
            ),
            "image_key": "printwriter_response",
            "links": [
                (
                    "https://jakarta.ee/specifications/servlet/6.0/",
                    "Jakarta Servlet — HttpServletResponse",
                ),
                (
                    "https://www.baeldung.com/java-printwriter",
                    "Baeldung: Guide to PrintWriter",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(string.concat|StringBuilder|StringBuffer|immutable.string)\b",
        {
            "name": "Java String Handling & Concatenation",
            "explanation": (
                "Java `String` objects are **immutable** — every concatenation with `+` "
                "creates a new `String` behind the scenes. For a small number of "
                "concatenations the compiler optimises via `StringBuilder`, but in loops "
                "you should use `StringBuilder` explicitly to avoid O(n²) copying. "
                "`StringBuffer` is the thread-safe (synchronised) variant, rarely needed "
                "in modern code."
            ),
            "image_key": "java_strings",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/data/strings.html",
                    "Oracle Java Tutorials — Strings",
                ),
                (
                    "https://www.baeldung.com/java-string-builder-string-buffer",
                    "Baeldung: StringBuilder vs StringBuffer",
                ),
            ],
        },
    ),
    (
        r"(?i)\b(data.?types?|primitiv)\b|\b(int|double|float|char|long|boolean|byte|short)\b",
        {
            "name": "Java Primitive Data Types",
            "explanation": (
                "Java has eight primitive types:\n\n"
                "• **Integers:** `byte` (8-bit), `short` (16-bit), `int` (32-bit), "
                "`long` (64-bit)\n"
                "• **Floating-point:** `float` (32-bit), `double` (64-bit)\n"
                "• **Character:** `char` (16-bit Unicode)\n"
                "• **Boolean:** `boolean` (`true`/`false`)\n\n"
                "Primitives are stored on the stack (or inlined) and are much faster "
                "than their wrapper counterparts. Literal suffixes like `f`, `L`, `d` "
                "disambiguate types."
            ),
            "image_key": "java_primitives",
            "links": [
                (
                    "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html",
                    "Oracle Java Tutorials — Primitive Data Types",
                ),
                (
                    "https://www.baeldung.com/java-primitives",
                    "Baeldung: Java Primitive Types",
                ),
            ],
        },
    ),
]

def _run(cmd):
    """Run a shell command and return its stdout as a stripped string.

    stderr is intentionally not suppressed so that git errors surface in the
    GitHub Actions log and provide actionable diagnostic information.
    """
    return subprocess.check_output(cmd, text=True).strip()


def get_commit_info():
    sha = _run(["git", "log", "-1", "--format=%H"])
    short_sha = sha[:7]
    message = _run(["git", "log", "-1", "--format=%s"])
    author = _run(["git", "log", "-1", "--format=%an"])
    date = _run(["git", "log", "-1", "--format=%ci"])[:10]  # YYYY-MM-DD
    return sha, short_sha, message, author, date


def get_diff():
    """Return the unified diff of the latest commit.

    Uses --unified=3 (three lines of context) to improve pattern-matching
    accuracy for multi-line constructs while keeping diff size manageable.
    For merge commits, falls back to diffing against the first parent so that
    the actual changes are visible rather than an empty diff.
    """
    try:
        diff = _run(["git", "show", "HEAD", "--unified=3"])
        # Merge commits often produce an empty diff with git show; fall back
        # to an explicit diff against the first parent.
        if not _has_meaningful_diff(diff):
            diff = _run(["git", "diff", "HEAD~1..HEAD", "--unified=3"])
        return diff
    except subprocess.CalledProcessError:
        return ""


def _has_meaningful_diff(diff_text):
    """Return True if diff_text contains at least one added/removed line."""
    for line in diff_text.splitlines():
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
            return True
    return False


def _extract_added_lines(diff_text):
    """Return only the added lines from a unified diff.

    Lines starting with ``+`` (but not ``+++``) represent content that is
    genuinely new in this commit.  Extracting only these lines ensures that
    concept detection is limited to what was actually introduced, rather than
    the entire file contents.
    """
    added = []
    for line in diff_text.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])  # strip the leading '+'
    return "\n".join(added)


# ---------------------------------------------------------------------------
# Concept detection
# ---------------------------------------------------------------------------

def _extract_comments(text):
    """Extract single-line (//) and block (/* */) comments from source text.

    This dedicated extraction ensures that shorthand notes like "IOC?" or
    "tight coupling" written inside comments are matched by the general
    concept registry even when the surrounding code does not contain a
    recognisable annotation or API call.
    """
    comments = []
    # Single-line comments
    comments.extend(re.findall(r"//[^\n]*", text))
    # Block comments (non-greedy)
    comments.extend(re.findall(r"/\*.*?\*/", text, re.DOTALL))
    return "\n".join(comments)


def detect_concepts(diff_text, commit_message):
    """Return a list of concept dicts found in the diff's added lines and commit message.

    Only the **added lines** (``+`` lines) from the diff are scanned so that
    concepts already present in the codebase are not re-reported.  Detection
    happens in two passes:
      1. **Code patterns** (CONCEPT_REGISTRY) — matched against added lines
         and the commit message.
      2. **Comment / keyword patterns** (GENERAL_CONCEPT_REGISTRY) — matched
         against the same text so that shorthand notes, questions, and
         explanations in code comments are detected.
    """
    added_lines = _extract_added_lines(diff_text)
    combined = added_lines + "\n" + commit_message
    detected = []
    seen = set()

    # Pass 1: code-level patterns
    for pattern, concept in CONCEPT_REGISTRY:
        if re.search(pattern, combined) and concept["name"] not in seen:
            detected.append(concept)
            seen.add(concept["name"])

    # Pass 2: comment / keyword patterns (scanned against full text so that
    # both code and comments are covered)
    for pattern, concept in GENERAL_CONCEPT_REGISTRY:
        if re.search(pattern, combined) and concept["name"] not in seen:
            detected.append(concept)
            seen.add(concept["name"])

    return detected


# ---------------------------------------------------------------------------
# Entry generation
# ---------------------------------------------------------------------------

def _count_existing_entries():
    if not os.path.exists(KNOWLEDGE_POOL_FILE):
        return 0
    with open(KNOWLEDGE_POOL_FILE, "r", encoding="utf-8") as fh:
        return len(re.findall(r"^## Entry #\d+", fh.read(), re.MULTILINE))


def generate_entry(short_sha, message, author, date, concepts):
    entry_num = _count_existing_entries() + 1
    lines = [
        "",
        "---",
        "",
        f"## Entry #{entry_num} — {date} | Commit: `{short_sha}` — {message}",
        "",
        f"> **Author:** {author}",
        "",
    ]

    if not concepts:
        lines += [
            "### Summary",
            "",
            "No specific Spring Boot or Java framework patterns were detected in this "
            "commit's diff. The commit may contain configuration, documentation, or "
            "infrastructure changes.",
            "",
        ]
    else:
        lines += ["### Concepts Introduced", ""]
        for concept in concepts:
            lines += [
                f"#### {concept['name']}",
                "",
                concept["explanation"],
                "",
                "**References:**",
            ]
            for url, title in concept["links"]:
                lines.append(f"- [{title}]({url})")
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

def _ensure_docs_dir():
    os.makedirs(DOCS_DIR, exist_ok=True)


def _initialise_file_if_needed():
    if not os.path.exists(KNOWLEDGE_POOL_FILE):
        header = (
            "# Knowledge Pool\n\n"
            "This file is automatically maintained by the "
            "[`update-knowledge-pool`](.github/workflows/update-knowledge-pool.yml) "
            "GitHub Actions workflow.\n\n"
            "Each entry is generated on every push to `main`, summarising the Spring Boot "
            "and Java concepts introduced in that commit.\n"
        )
        with open(KNOWLEDGE_POOL_FILE, "w", encoding="utf-8") as fh:
            fh.write(header)


def _append_entry(entry):
    with open(KNOWLEDGE_POOL_FILE, "a", encoding="utf-8") as fh:
        fh.write(entry + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    _ensure_docs_dir()
    _initialise_file_if_needed()

    sha, short_sha, message, author, date = get_commit_info()
    diff = get_diff()
    concepts = detect_concepts(diff, message)
    entry = generate_entry(short_sha, message, author, date, concepts)
    _append_entry(entry)

    total = _count_existing_entries()
    print(f"Knowledge Pool entry #{total} appended for commit {short_sha} — '{message}'.")
    if concepts:
        print(f"  Detected concepts: {', '.join(c['name'] for c in concepts)}")
    else:
        print("  No Spring/Java patterns detected in this commit.")


if __name__ == "__main__":
    main()
