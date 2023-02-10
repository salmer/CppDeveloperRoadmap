# :ghost: Myths and Legends of C++

## :question: C++ is dead, it's impossible to code anything with it

C++'s not dead.

In fact, it has consistently ranked among the top programming languages in various ratings, such as the [Tiobe](https://www.tiobe.com/tiobe-index/) index. The perception that C++ is a "dead language" emerged during the early 2000s, when the language standardization committee was inactive. However, C++ has since undergone a resurgence, with new features and functionality being added every three years since the C++11 standard. Despite this, there are still those who perpetuate the myths and legends of C++ being a difficult and problematic language, often because they haven't kept up with the developments in the language or have only had limited exposure to it in their education.

## :question: Real programmers learn C++ using Linux/Vim/gcc

If you are not familiar with the mentioned combination, it is recommended to focus on learning the basics of C++ first. It is suggested to start developing your first applications using Microsoft Visual Studio IDE. For more information, see the [PreJunior Books](Books/PreJunior.md).

Taking the challenging path may seem cool, but there is a high probability that the amount of information needed to create a "Hello World" program using Linux, Vim, and GCC will be overwhelming. This could lead to early frustration and disillusionment with programming as a whole. Try to follow a path that starts with simple things and gradually increases in complexity. Just like a novice shouldn't try to lift the heaviest weights during their first workout, the same rule applies to learning. Once you are comfortable with the language, you can try developing using Linux. But that is a different story altogether...

## :question: You'd better master C/Assembler/etc. before learning C++

No, no, and no again!

This statement persists due to two widespread scenarios: it's how C++ was taught in universities in the past, and members of the "Old Guard" went through a similar path. Modern C++ does not require such a challenging approach. The language is self-sufficient and can be learned without any prior background. It's more likely that learning C++ through the "C -> C++" approach will result in confusion and a desire to write C++ in a "C with classes" style.

## :question: Learn C++ using the book by Stroustrup

A highly damaging statement that originates from the "Old Guard" or those who were born with a keyboard in hand.

This piece of advice is likely given by those who have extensive experience in developing other languages (such as C, Fortran, Delphi, etc.) and then transitioned to C++. Stroustrup wrote the book [The C++ Programming Language](https://www.amazon.com/C-Programming-Language-4th/dp/0321563840) as a reference, so it must be used in an appropriate manner, which requires some knowledge of the language. Instead, it's better to look at the [Books](Books/Overview.md) section, where you'll find books for all levels of language proficiency.

## :question: Learn C++ using the Standard only

Another snobbish statement.

The modern C++ standard, which exceeds 2000 pages, requires payment for access to the up-to-date version and is not composed in a user-friendly manner. While it is commendable for those who learned the language using its standard, it is not recommended as a way to learn for most individuals. Instead, it's better to check out the [Books](Books/Overview.md) section, where you'll find books suitable for various levels of language proficiency.

## :question: Undefined Behavior haunts the developer everywhere

More likely no than yes.

Modern C++ and the tooling that has emerged around the language allow avoiding the lion's share of problems related to undefined behavior. We can give a simple piece of advice: when unsure what a particular construct does, read about it on [CppReference](https://en.cppreference.com), [StackOverflow](https://stackoverflow.com/) or other dedicated resources. If you're still in doubt after reading, try rewriting the code in a simpler manner to avoid undefined behavior. There lies great power in simplicity.

## :question: One needs to manage memory manually, there is no garbage collection in the language

This is another urban legend from the "Old Guard," who stopped writing C++ before C++11 or those who superficially learned it in university and disregarded the latest standards. Modern C++ has a set of primitives in its standard library that are responsible for automatic memory allocation and deallocation. Manual memory management has fallen by the wayside. Many teams and companies even have the rule: "No raw pointers." Once again, do not neglect the modern tools and sanitizers, as they can detect possible memory leaks at the source code level.

## :question: C++ is legacy area only

Partially, it's true, but it's worth noting that it's not only applicable to C++. The code quality in any language mainly depends on the technical culture of a team and its pioneers, not just the language. The majority of legacy code is produced due to human factors: the developer's skill level, work ethic, and incorrect estimations, among others. Nowadays, there are many projects written in C++ that have been working 24/7 for years and are the foundation of a company's revenue. In such cases, it's dangerous to make any significant changes in a short period. The developers take great care when making changes to avoid any regressions. However, don't think that working on legacy projects cannot help you improve. In fact, these projects can provide a challenge that can give you a wealth of experience in areas such as code reading, reverse engineering, testing, software architecture design, automation, and requirements gathering, among others.

---

[**To main page**](../README.md)