# :scales: Coding standards and regulatory requirements

C++ has traditionally occupied the areas where the cost of a mistake is measured not in lost money but in human lives: automotive electronics, medical devices, avionics, industrial automation, rail transport. In such projects the freedom of the language becomes a problem, so it is constrained — with a body of coding rules, mandatory checks, and a documented development process.

This article is an overview map of the territory, not a certification guide. Its goal is for you to understand what is meant when a job posting says "MISRA experience" or "ISO 26262 projects," and to know where to look for the details.

There are a great many standards and requirements, and only the most prominent are collected below. There is no single "mandatory set": every project uses its own subset depending on the industry, country, customer, and criticality class. It makes sense to dig into a specific standard when you actually meet it on your project, not just in case.

> :warning: Requirements and deadlines change. Before making decisions, check against the current editions of the standards and with your company's lawyers — this article is for orientation, not for legal conclusions.

## :straight_ruler: Coding standards

They restrict the language to a subset with fewer ways to shoot yourself in the foot: no dynamic memory allocation after initialization, no exceptions, no implicit type conversions, and so on. Compliance is verified by static analyzers — such rule sets are not checked by hand.

* :arrow_forward: **MISRA C++:2023** - [misra.org.uk](https://misra.org.uk)

    The best-known rule set for C++ in safety-critical systems. It replaced MISRA C++:2008 and covers C++17. An important change: it absorbed the **AUTOSAR C++14** guidelines, so instead of two competing rule sets, as before, there is now a single one moving forward. If you come across a project on AUTOSAR C++14, that is the previous generation of the same approach ([autosar.org](https://www.autosar.org)).

* :arrow_forward: **SEI CERT C++** - [wiki.sei.cmu.edu](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682)

    A rule set with an emphasis on security: how to avoid constructs that lead to vulnerabilities. Unlike MISRA, it is available free and openly — a good way to get acquainted with the genre itself, even if your project is not being certified.

* :arrow_forward: **C++ Core Guidelines** - [isocpp.github.io](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

    Guidelines from Bjarne Stroustrup and Herb Sutter. Unlike MISRA, they do not restrict the language but rather nudge you toward a modern style. Formally they are not a regulatory document, but they are useful to any C++ developer; they are partially checkable via `clang-tidy` and the [Microsoft GSL](https://github.com/microsoft/GSL).

## :shield: Functional safety

These answer the question "what must happen so that the system does no harm in the event of a failure." They regulate not so much the code as the process: requirements, traceability, testing, documentation, and qualification of the tools used.

The base standard in this area is **IEC 61508**, which introduces the Safety Integrity Levels SIL 1-4. The industry standards below are its adaptations:

* :arrow_forward: **ISO 26262** - automotive - [iso.org](https://www.iso.org/standard/68383.html)

    Functional safety of road vehicles. It introduces the ASIL levels from A to D, where D is the strictest (for example, brake or steering control). This is where the "ISO 26262 + MISRA C++" pairing is encountered most often.

* :arrow_forward: **IEC 62304** - medical software - [iso.org](https://www.iso.org/standard/38421.html)

    The software life cycle for medical devices. It defines safety classes A, B, and C depending on whether a failure can lead to harm to health and how severe. Compliance with this standard is the main way to demonstrate conformity with the European Medical Device Regulation **MDR** ([Regulation (EU) 2017/745](https://eur-lex.europa.eu/eli/reg/2017/745/oj)), as well as with FDA requirements in the US.

* :arrow_forward: **DO-178C** - avionics - [rtca.org](https://www.rtca.org)

    Requirements for airborne software. The DAL criticality levels run from A to E; level A requires, among other things, test coverage at the level of individual conditions within logical expressions (MC/DC). It is considered one of the most demanding and expensive standards in the industry to comply with.

## :lock: Cybersecurity and the supply chain

A relatively new topic for the C++ world: regulators are shifting responsibility for vulnerabilities onto the software vendor.

* :arrow_forward: **EU Cyber Resilience Act (CRA)** - [digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act)

    An EU regulation covering products with digital elements supplied to the European market — from industrial controllers to consumer electronics. It requires secure development, the release of security updates throughout the support period, and notification of actively exploited vulnerabilities. It entered into force in December 2024, with the main obligations applying from the end of 2027 and the notification obligations earlier. Importantly, it affects not only "safety-critical" industries but practically any software that is part of a product being sold.

* :arrow_forward: **SBOM (Software Bill of Materials)** - [spdx.dev](https://spdx.dev), [cyclonedx.org](https://cyclonedx.org)

    A machine-readable inventory of all components and dependencies that go into the delivered software — the "list of ingredients," by analogy with a label on a package. It is needed so that when a vulnerability is found in a popular library, you can quickly answer the question "do we have it?" The two main formats are SPDX and CycloneDX; both are standardized. For C++ the topic is tangible: dependencies are often pulled in as source or built by hand, and without an SBOM it is not always obvious what exactly ended up in the build.

## :computer: What this means in practice

If you land on such a project, what changes is not so much the language as the environment around the code:

- **A language subset.** Some familiar features will be forbidden — usually dynamic memory after initialization, exceptions, RTTI, and sometimes templates and the standard library as a whole.
- **Mandatory static analysis.** The build fails not only on compiler errors but on rule violations. Deviations from the rules are documented and agreed upon in writing, not simply suppressed in the code.
- **Traceability.** For every line of code you can trace which requirement it came from and which test covers it. Hence the high demands on how tasks and commits are written up.
- **Tool qualification.** The compiler, analyzer, and testing framework must be justified too — which is why versions are updated rarely, and "just grab the latest GCC" is not always possible.
- **Heavy review and documentation.** The volume of accompanying documents can exceed the volume of code, and timelines can noticeably exceed those of ordinary development.

## :question: Who actually needs this

**Not everyone.** If you write games, desktop applications, backends, or trading systems, in practice you most likely will not encounter these standards, and there is no point studying them specially.

The topic becomes mandatory if you go into automotive electronics, medical devices, aviation, space, rail transport, or industrial automation. For everyone else it is enough to know that these standards exist and what they are about — that is enough for an interview.

The exception is **CRA and SBOM**. They concern a far wider range of products than classic functional safety, so it is worth getting acquainted with them even as an "ordinary" developer whose products are sold in Europe.

---

[**To main page**](../README.md)
