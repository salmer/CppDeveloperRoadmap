# Myths and Legends of C++

## C++ is dead, it's impossible to code anything with it

C++'s not dead.

C++ made its way to the top of a wide range of ratings of programming languages, and it is scoring, moreover, popularity points, for example in the [Tiobe](https://www.tiobe.com/tiobe-index/) index. C++ got its notorious "dead language" badge during the noughties, while it was dormant and the language standardization committee fell off the radar. But the language is experiencing a renaissance since the C++11 standard. It is arduously getting new features and functionality, every three years. Many problems claimed by the "dead C++ witnesses" have been solved, but since such specialists have stopped developing using C++ - or got a smattering of C++ during courses (from those very "witnesses") - they continue repeating and reiterating the myths and legends of the horrors of C++. 

## Real programmers learn C++ using Linux/Vim/gcc

If you are unfamiliar with the aforementioned combo, we recommend you concentrate on learning the basics of C++ alone. We also suggest you start developing your first applications using Microsoft Visual Studio IDE (see [PreJunior Books](Books/PreJunior.md) for the details).

Choosing the hard way looks cool, but there is a high chance that the volume of the information needed to build the "Hello World" using Linux + Vim + gcc would be overwhelming. It is fraught with an early frustration and disaffection with programming as a whole. Try to follow the path from simple to complicated. Novices don't try to lift the heaviest weights during the first workout because they know what it might lead to. The same rule applies to education. You can try developing under Linux once you are comfortable with the language. But it's a different story altogether...

## You'd better master C/Assembler/etc. before learning C++

No, no, and no again! 

This statement continues to live due to two widespread scenarios: it's how they used to teach in the university, and the members of the "Old Guard" went through a similar path. Modern C++ doesn't require such torture. This language is self-sufficient and can be learned with no background whatsoever. It's more likely that learning the "C -> C++" way you get a mess in your head and a firm desire to write C++ in the "C with classes" style.

## Learn C++ using the book by Stroustrup

A highly damaging thesis taking origin from the "Old Guard" or someone born with a keyboard in hand.

Those who had extensive experience of development in other languages (C, Fortran, Delphi, etc.) and transitioned to C++ are most likely to give this piece of advice. Stroustrup wrote this book like a reference, therefore one needs to use it in the appropriate manner, which requires some knowledge of the language. Better look at the [Books](Books/Overview.md) section, you'll find books for any level of language proficiency.

## Learn C++ using the Standard only

Another snobbish statement.

First, the modern C++ standard exceeds 2000 pages. Secondly, the access to the up-to-date version requires payment. Thirdly, the standard isn't composed in a friendly way. Those who learned the language using its standard can be pat on the back, but we do not recommend abusing oneself this way. Once again, better look at the [Books](Books/Overview.md) section, you'll find books for any level of language proficiency.

## Undefined Behavior haunts the developer everywhere

More likely no than yes.

Modern C++ and the tooling emerged around the language allow to avoid the lion's share of the problems related to the undefined behavior. We can give a rather simple piece of advice: when hesitant what a particular construct does, read about it on [CppReference](https://en.cppreference.com), [StackOverflow](https://stackoverflow.com/) or other dedicated resources. If still in doubt after the reading, try rewriting the code in a simpler manner to avoid the undefined behavior. In simplicity there lies a great power.

## One needs to manage memory manually, there is no garbage collection in the language

This is another urban legend from the "Old Guard" that had stopped writing C++ before C++11 or those who superficially learned it in university disregarding the latest standards. Modern C++ contains a set of primitives in its standard library which are responsible for the automatic memory allocation and deallocation. The manual memory management fell by the wayside. Many teams and companies even have the rule: "No raw pointers". Once again, do not neglect the modern tools and sanitizers: they can detect possible memory leaks at the source code level.

## C++ is legacy area only

Partially it's true, but it's good to note that it's applicable for other languages. Even with a modern stack, developers can produce code that will become legacy very fast. The code quality mainly depends on the technical culture of a team and its pioneers, not a language. The majority amount of legacy code is produced under the human factor: developer's grade and skill set, work ethic, wrong estimations, etc. Nowadays, you can meet a lot of projects working 24/7 for years and written in C++. Such kinds of systems are often the business foundation of revenue. In this case, it's really dangerous to perform any huge changes in short time. The developers make any changes with high attention to any regression. But don't think that legacy projects can not help you to improve yourself. In fact, these projects can give you a challenge that can bring you widespread experience in different areas: code reading, reverse-engineering, testing, designing of SW architecture, automation, requirements gathering, etc.