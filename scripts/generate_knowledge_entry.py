#!/usr/bin/env python3
"""Analyze the latest git commit and append a learning entry to docs/Knowledge_Pool.md."""

import subprocess
import re
import os
from datetime import datetime

DOCS_DIR = "docs"
KNOWLEDGE_POOL_FILE = os.path.join(DOCS_DIR, "Knowledge_Pool.md")

# ---------------------------------------------------------------------------
# Concept registry
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
        r"(Inversion of Control|IoC|interface\b.*\bimplements\b|\bimplements\b.*Service)",
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
# Git helpers
# ---------------------------------------------------------------------------

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


def get_changed_files_content():
    """Return the full content of source files changed in the latest commit.

    This allows the detector to find patterns in comments, imports, and
    surrounding context that may not appear in the narrow diff window.
    """
    try:
        files = _run(
            ["git", "diff-tree", "--no-commit-id", "-r", "--name-only", "HEAD"]
        )
        if not files:
            # For merge commits, compare against the first parent.
            files = _run(["git", "diff", "--name-only", "HEAD~1..HEAD"])
    except subprocess.CalledProcessError:
        return ""

    contents = []
    for filepath in files.splitlines():
        filepath = filepath.strip()
        if not filepath:
            continue
        try:
            content = _run(["git", "show", f"HEAD:{filepath}"])
            contents.append(content)
        except subprocess.CalledProcessError:
            # File may have been deleted in this commit.
            continue
    return "\n".join(contents)


# ---------------------------------------------------------------------------
# Concept detection
# ---------------------------------------------------------------------------

def detect_concepts(diff_text, commit_message, changed_files_content=""):
    """Return a list of concept dicts whose patterns match the diff, commit message, or changed file contents.

    Scanning the full content of changed files (not just the diff) ensures
    that patterns inside code comments, imports, and surrounding context are
    detected even when they fall outside the narrow diff window.
    """
    combined = diff_text + "\n" + commit_message + "\n" + changed_files_content
    detected = []
    seen = set()
    for pattern, concept in CONCEPT_REGISTRY:
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
                (
                    f'<img src="assets/{concept["image_key"]}.png" '
                    f'alt="{concept["name"]} diagram" width="600"/>'
                ),
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
    changed_content = get_changed_files_content()
    concepts = detect_concepts(diff, message, changed_content)
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
