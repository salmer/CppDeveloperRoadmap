# Canonical roadmap source. This file is the STRUCTURE of the map for every language;
# the words live in en.tsv / ru.tsv / zh.tsv, keyed by the same [word-id].
# Edit this file -- never the generated <Lang>/Graph/roadmap.drawio.svg.
#
# Quick reference (full grammar: tools/mapgen/README.md):
#   [id] grade=... stage=N side=left|right   a node; 2 spaces of indent = one level deeper
#     grade  junior | middle | senior | optional   -> the box colour
#     stage  1..5, inherited by the subtree        -> wraps it in a grey "N step" frame
#     side   left | right, inherited               -> which half of the spine it hangs off
#   hint [id] angle=<deg> dist=<px> arrow=<side> -> target, target
#     a pink note; angle 0=right 90=up 180=left 270=down, dist in map units,
#     arrow = which edge of the note the arrow leaves from (required)
#   spine center=<id>                        the central trunk both halves centre on
#
# Adding a node = one line here + one row in EACH of en/ru/zh.tsv, then rebuild:
#   python tools/mapgen/setup.py --venv        # first time only
#   python tools/mapgen/build.py --dir tools/mapgen/roadmap --deploy --check
#
# Seeded from the hand-drawn EN map by tools/mapgen/bootstrap/extract.py; hand-maintained since.

spine center=cpp-developer

[soft-skills] side=left grade=junior
  [ability-to-learn] grade=junior
    [ask-the-right-questions] grade=junior
    [process-information] grade=junior
    [experimenting] grade=middle
    [manage-knowledge] grade=senior
  [manage-mistakes] grade=junior
    [analyze-mistakes] grade=junior
    [admitting-your-mistakes] grade=junior
    [notify-about-mistakes-in] grade=junior
    [accept-criticism] grade=junior
  [thinking] grade=junior
    [logical] grade=junior
    [systems] grade=middle
    [critical] grade=middle
    [creative] grade=middle
    [strategic] grade=senior
  [responsibility] grade=junior
    [discipline] grade=junior
    [persistence] grade=junior
    [initiative] grade=middle
    [independence] grade=middle
    [problem-solving] grade=middle
  [manage-resources] grade=junior
    [time-management] grade=junior
    [prioritization] grade=junior
    [taking-decisions] grade=middle
    [blind-typing] grade=middle
    [multitasking] grade=senior
  [communication] grade=junior
    [negotiation] grade=junior
      [ability-to-listen] grade=junior
      [persuasion] grade=middle
      [ability-to-communicate-ideas] grade=middle
        [providing-information-to-people] grade=senior
      [finding-compromises] grade=senior
      [dispute-resolution] grade=senior
    [english] grade=junior
    [presentation] grade=middle
    [written-communication-skill] grade=middle
    [networking] grade=senior
  [team-work] grade=junior
    [understanding-the-distribution-of] grade=junior
    [support-team-members] grade=middle
    [work-in-a-distributed] grade=middle
    [providing-feedback] grade=middle
    [leadership] grade=senior
      [assigning-and-clarifying-tasks] grade=senior
      [planning-and-goal-setting] grade=senior
    [mentoring] grade=senior
    [delegation] grade=senior
  [emotional-intelligence] grade=junior
    [stress-resistance] grade=junior
      [working-in-uncertainty] grade=junior
    [adaptability] grade=junior
    [open-mindedness] grade=junior
    [concentration] grade=junior
    [empathy] grade=middle
  [understanding-the-development-context] grade=middle
    [customer-focus] grade=senior
    [technology] grade=senior
    [trends] grade=senior

[hard-skills] side=right grade=junior
  [language-syntax] grade=junior
    [basic-operations] grade=junior stage=1
      [arithmetic-operations] grade=junior
      [logical-operations] grade=junior
      [loops-for-while] grade=junior
      [bitwise-operations] grade=middle
    [functions] grade=junior stage=1
      [operators] grade=middle
      [lambda] grade=middle
    [data-types] grade=junior stage=1
      [static-typing] grade=middle
      [dynamic-typing] grade=middle
        [rtti] grade=middle
    [pointers-and-references] grade=junior stage=1
      [references] grade=junior
      [smart-pointer] grade=junior
        [unique-ptr] grade=junior
        [shared-ptr] grade=junior
        [weak-ptr] grade=middle
      [memory-model] grade=junior
        [lifetime-of-objects] grade=junior
      [raw-pointers] grade=junior
        [new-delete-operators] grade=junior
        [memory-leakage] grade=junior
    [codebase-structuring] grade=junior stage=1
      [code-splitting-into-headers] grade=junior
        [forward-declaration] grade=junior
      [scope] grade=junior
        [namespaces] grade=junior
    [structures-and-classes] grade=junior stage=2
      [object-oriented-programming] grade=junior
        [static-polymorphism] grade=junior
          [overloading-of-functions] grade=junior
        [dynamic-polymorphism] grade=junior
          [virtual-methods] grade=junior
          [virtual-table] grade=junior
      [the-rule-of-zero] grade=middle
      [multiple-inheritance] grade=middle
        [diamond-inheritance] grade=middle
    [exception-handling] grade=junior stage=2
      [std-optional-std-expected] grade=middle
      [exceptions] grade=junior
        [access-violation] grade=junior
      [noexcept] grade=middle
      [error-codes] grade=optional
        [std-error-code] grade=optional
    [language-concepts] grade=junior stage=3
      [auto] grade=junior
      [type-casting] grade=junior
        [static-cast] grade=junior
        [const-cast] grade=junior
        [dynamic-cast] grade=middle
        [reinterpret-cast] grade=middle
      [undefined-behavior] grade=middle
      [argument-dependent-lookup] grade=middle
      [constexpr-consteval] grade=middle
      [macros] grade=senior
      [name-mangling] grade=optional
      [move-semantics] grade=middle
        [value-categories] grade=middle
        [std-move-std-forward] grade=middle
        [perfect-forwarding] grade=senior
      [coroutines] grade=senior
      [modules] grade=optional
    [standard-library-stl] grade=junior stage=3
      [iostream] grade=junior
        [std-format-std-print] grade=middle
      [date-time] grade=junior
      [containers] grade=junior
        [std-span-std-string] grade=middle
      [iterators] grade=junior
      [algorithms] grade=junior
        [std-ranges] grade=senior
      [multithreading] grade=middle
    [templates] grade=junior stage=4
      [variadic-templates] grade=middle
      [the-template-specialization] grade=middle
        [the-full-template-specialization] grade=middle
        [the-partial-template-specialization] grade=middle
      [type-traits] grade=senior
      [sfinae] grade=senior
      [concepts] grade=middle
    [idioms] grade=junior stage=4
      [raii] grade=junior
      [pimpl] grade=middle
      [non-copyable-non-moveable] grade=middle
      [erase-remove] grade=middle
      [copy-and-swap] grade=middle
      [copy-on-write] grade=middle
      [crtp] grade=middle
    [standards] grade=junior stage=4
      [cpp11-14] grade=junior
      [cpp17] grade=junior
      [cpp20] grade=middle
      [cpp23] grade=senior
      [cpp26] grade=optional
  [language-tools] grade=junior
    [working-with-source-code] grade=junior stage=1
      [text-editors] grade=junior
      [ide] grade=junior
      [code-editors] grade=junior
        [knowledge-of-features-and] grade=junior
      [debugger] grade=junior
        [understanding-of-debugger-messages] grade=junior
        [debugging-symbols] grade=junior
        [windbg] grade=optional
        [gdb] grade=optional
        [lldb] grade=optional
      [linters] grade=middle
      [compiler-explorer] grade=optional
    [compilers] grade=junior stage=3
      [basic-understanding-of-compilers] grade=junior
        [compilation-of-sources-to] grade=junior
        [the-object-files-linkage] grade=junior
        [working-stages-of-compilers] grade=senior
      [features-of-a-particular] grade=optional
    [build-systems] grade=junior stage=5
      [cmake] grade=middle
      [makefile] grade=optional
      [ninja] grade=optional
    [package-managers] grade=junior stage=5
      [conan] grade=optional
      [nuget] grade=optional
      [vcpkg] grade=optional
      [spack] grade=optional
    [working-with-libraries] grade=junior stage=5
      [libraries-inclusion] grade=junior
      [licensing] grade=optional
    [libraries] grade=junior stage=5
      [boost] grade=middle
      [opencv] grade=optional
      [poco] grade=optional
      [protobuf] grade=optional
      [asio] grade=optional
      [grpc] grade=optional
      [fmt] grade=optional
      [nlohmann-json] grade=optional
      [pybind11] grade=optional
      [spdlog] grade=optional
      [range-v3] grade=optional
      [tensorflow] grade=optional
      [opencl] grade=optional
    [frameworks] grade=junior stage=5
      [gtest-gmock] grade=middle
      [qt] grade=optional
      [catch2] grade=optional
      [google-benchmark] grade=optional
      [google-profiler] grade=optional
      [pytorch-cpp] grade=optional
  [common-skills] grade=junior
    [computers-science] grade=junior stage=1
      [data-structures] grade=junior
      [boolean-algebra] grade=junior
      [computers-science-algorithms] grade=middle
      [finite-state-machines] grade=middle
    [version-control-software] grade=junior stage=4
      [distributed] grade=optional
        [git] grade=junior
        [mercurial] grade=optional
      [centralized] grade=optional
        [svn] grade=optional
    [best-practices] grade=junior stage=4
      [code-quality] grade=junior
        [code-guidelines] grade=junior
        [principles-of-development] grade=junior
          [kiss] grade=junior
          [dry] grade=junior
          [yagni] grade=junior
          [apo] grade=junior
          [bduf] grade=middle
          [composition-is-preferably-than] grade=middle
          [occam-s-razor] grade=middle
          [divide-and-conquer] grade=middle
        [logging-and-telemetry] grade=junior
        [code-review] grade=junior
          [skill-to-read-existing] grade=junior
          [skill-to-review-code] grade=middle
        [lifecycle-stages-of-a] grade=junior
          [implementation] grade=junior
          [testing] grade=junior
            [unit-tests] grade=junior
            [integration-tests] grade=junior
            [functional-tests] grade=junior
            [performance-tests] grade=middle
          [maintanance] grade=junior
          [versioning] grade=junior
            [backward-compatibility] grade=junior
          [software-architecture-and-components] grade=middle
          [components-integration] grade=middle
          [deployment] grade=middle
          [collecting-requirements] grade=senior
          [end-of-a-software] grade=senior
        [code-analyzers] grade=middle
          [static-analyzers] grade=middle
          [dynamic-analyzers] grade=middle
            [profilers] grade=middle
              [valgrind] grade=optional
              [perf-vtune] grade=optional
        [cpp-core-guidelines] grade=optional
          [microsoft-gsl] grade=optional
        [industrial-standards] grade=optional
          [misra-cpp-2023] grade=optional
          [autosar] grade=optional
          [eu-cyber-resilience-act] grade=optional
          [sbom] grade=optional
          [iec-62304] grade=optional
          [iso-26262] grade=optional
          [do-178c] grade=optional
      [command-line] grade=junior
        [powershell] grade=optional
        [batch] grade=optional
        [bash] grade=optional
      [ci-cd] grade=junior
        [creation-of-a-software] grade=junior
          [documentation] grade=junior
          [installer-package] grade=junior
        [trunk-based-development] grade=optional
        [zero-downtime-deployment] grade=optional
      [ai-tools] grade=junior
        [ai-assistants] grade=junior
        [verifying-generated-code] grade=junior
        [company-policy-and-confidentiality] grade=junior
        [licensing-risks-of-generated] grade=middle
        [local-models] grade=optional
      [usage-of-other-programming] grade=middle
      [language-interoperability] grade=middle
    [software-design] grade=junior
      [design-patters] grade=middle stage=2
        [structural] grade=middle
        [behavioral] grade=middle
        [creational] grade=middle
      [oop] grade=junior stage=2
        [solid] grade=middle
      [uml] grade=middle stage=2
      [architecture-styles] grade=senior
        [component-based] grade=senior
        [monolithic-application] grade=senior
        [layered] grade=senior
        [client-server] grade=senior
        [microservices-architecture] grade=senior
        [event-driven] grade=senior
        [plug-ins] grade=senior
        [rest] grade=senior
        [service-oriented-architecture] grade=senior
      [architecture-patterns] grade=senior
        [mvc] grade=senior
        [mvvm] grade=senior
        [three-tier] grade=senior
        [onion] grade=senior
        [hexagon] grade=senior
      [methodologies-of-development] grade=junior
        [test-driven-development] grade=junior
        [behavior-driven-development] grade=middle
        [domain-driven-design] grade=senior
  [operating-systems] grade=junior
    [binary-units] grade=junior
      [executable-file] grade=junior
      [static-library] grade=junior
      [dynamic-library] grade=junior
    [memory] grade=junior
      [memory-abstractions] grade=junior
        [stack] grade=junior
        [heap] grade=junior
        [global-memory] grade=middle
        [application-memory] grade=middle
      [memory-alignment] grade=middle
      [memory-management] grade=senior
      [virtual-memory] grade=senior
    [threads] grade=junior
      [threads-multithreading] grade=junior
        [errors] grade=junior
          [dead-lock] grade=junior
          [race-condition] grade=junior
          [live-lock] grade=junior
          [starvation] grade=junior
        [std-atomic-cpp-memory] grade=senior
        [concurrency] grade=middle
          [mutexes] grade=middle
          [semaphores] grade=middle
          [lock-free] grade=middle
        [condition-variable] grade=middle
        [future-promise-async] grade=middle
        [jthread] grade=optional
        [event-handling] grade=middle
          [sync] grade=middle
          [async] grade=middle
        [openmp-tbb] grade=optional
    [process] grade=junior
      [interprocess-communication] grade=middle
        [shared-memory] grade=middle
        [pipes] grade=middle
        [serialization] grade=middle
          [json] grade=middle
          [xml] grade=optional
    [network] grade=junior
      [tcp-ip] grade=junior
        [sockets] grade=junior
          [tcp] grade=junior
          [udp] grade=junior
        [http] grade=middle
      [osi] grade=junior
    [file-system] grade=middle
    [task-scheduler] grade=senior
    [virtualization] grade=optional
      [virtualbox] grade=optional
      [vmware-workstation] grade=optional
      [hyper-v] grade=optional
      [virtualization-containers] grade=optional
        [docker] grade=optional
        [kubernetes] grade=optional
        [cloud-services] grade=optional
    [security] grade=optional
      [vulnerabilities-buffer-overflow-use] grade=middle
      [sanitizers] grade=middle
      [encryption] grade=optional
      [fuzzing] grade=optional
      [cert-cpp-cwe] grade=optional
    [multicpu-systems] grade=optional
      [multicore-cpu] grade=optional
      [numa] grade=optional
    [input-output] grade=optional
      [drivers] grade=optional
      [audio] grade=optional
        [directsound] grade=optional
        [openal] grade=optional
      [graphics] grade=optional
        [directx] grade=optional
        [opengl] grade=optional
        [vulkan] grade=optional
        [cuda] grade=optional
      [printers] grade=optional

# Hints (pink annotation boxes). Each sits at a polar offset from the mean centre of its
# target(s): angle in degrees (0 = right, 90 = up, 180 = left, 270 = down), dist in pixels
# (map coordinate units). `arrow=left|right|top|bottom` (required) sets which box edge the
# arrow starts from. Hand-tuned; keep `mapcheck` clean across all languages after edits.
hint [the-overloading-of-regular] angle=0 dist=500 arrow=left -> operators
hint [to-prevent-memory-leakage] angle=10 dist=400 arrow=left -> references, shared-ptr, unique-ptr
hint [it-s-preferred-to] angle=0 dist=388 arrow=left -> diamond-inheritance
hint [some-of-language-constructions] angle=0 dist=500 arrow=left -> undefined-behavior
hint [ability-to-gather-analyze] angle=180 dist=500 arrow=right -> process-information
hint [choose-one-of-the] angle=175 dist=350 arrow=right -> ide
hint [choose-one-of-the-2] angle=0 dist=450 arrow=left -> text-editors
hint [choose-one-of-the-3] angle=5 dist=590 arrow=left -> knowledge-of-features-and
hint [learn-about-common-errors] angle=356 dist=800 arrow=left -> understanding-of-debugger-messages
hint [reflection] angle=177 dist=400 arrow=right -> analyze-mistakes, admitting-your-mistakes
hint [study-how-to-use] angle=190 dist=330 arrow=right -> debugger
hint [the-ability-to-work] angle=3 dist=464 arrow=left -> windbg, gdb, lldb
hint [calmly-react-to-what] angle=190 dist=460 arrow=right -> accept-criticism
hint [the-compiler-performs-several] angle=356 dist=700 arrow=left -> working-stages-of-compilers
hint [take-challenging-tasks-in] angle=165 dist=400 arrow=right -> initiative
hint [each-compiler-has-its] angle=340 dist=600 arrow=left -> features-of-a-particular
hint [you-should-be-responsible] angle=189 dist=750 arrow=right -> independence
hint [carefully-read-the-terms] angle=0 dist=390 arrow=left -> licensing
hint [self-organization] angle=5 dist=350 arrow=left -> manage-resources
hint [the-ability-to-provide] angle=180 dist=533 arrow=right -> providing-information-to-people
hint [at-first-some-of] angle=305 dist=300 arrow=top -> soft-skills
hint [conflict-solving] angle=180 dist=312 arrow=right -> finding-compromises, dispute-resolution
hint [if-you-read-this] angle=335 dist=700 arrow=left -> english
hint [look-for-like-minded] angle=180 dist=635 arrow=right -> networking
hint [it-s-also-good] angle=0 dist=400 arrow=left -> computers-science-algorithms
hint [you-should-study-and] angle=180 dist=850 arrow=right -> adaptability
hint [experienced-developers-should-develop] angle=180 dist=500 arrow=right -> empathy
hint [to-configure-automated-code] angle=7 dist=500 arrow=left -> code-guidelines
hint [naming-conventions-tabs-vs] angle=190 dist=380 arrow=right -> code-guidelines
hint [do-not-ignore-warnings] angle=135 dist=250 arrow=bottom -> code-analyzers
hint [ai-can-generate-plausible] angle=170 dist=360 arrow=right -> ai-tools
hint [scripting-functional-sql-like] angle=5 dist=450 arrow=left -> usage-of-other-programming
hint [sometimes-it-s-needed] angle=355 dist=850 arrow=left -> language-interoperability
hint [memory-safety-requirements-are] angle=0 dist=720 arrow=left -> vulnerabilities-buffer-overflow-use
