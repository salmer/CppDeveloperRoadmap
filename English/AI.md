# :robot: The C++ developer and artificial intelligence

With the arrival of models that write code confidently, many aspiring developers have asked a reasonable question: is it even worth entering the profession? It is a fair question, and brushing it off with "nah, everything will be the same as before" would be wrong. Let's look at what is actually happening.

The short answer: engineers are still needed, but the bar has shifted. Here is why.

## :dna: AI reproduces what it was trained on

A model is trained on a vast body of already-written code, and by its very nature it produces what appeared most often in that data. It does an excellent job with tasks humanity has already solved thousands of times: parsing JSON, standing up an HTTP server, writing tests for an easy-to-understand function.

Its limitations grow from exactly the same root:

- **The unusual is handled poorly.** Your problem domain, your hardware constraints, the memory-versus-latency trade-off in your particular case — none of that was in the training data. And engineering work largely consists of these "but in our case everything is different" situations.
- **A bias toward old code.** Open-source C++ has accumulated over decades, and it is written predominantly in an older style. So models happily hand you `new`/`delete` instead of smart pointers, raw loops instead of algorithms, C-strings instead of `std::string_view`. The code will work, but it will not be the code you want to see in your project.
- **Confidence is not correctness.** A model may cite a nonexistent standard-library function or confuse the behavior of an overload — and state it in exactly the same tone as a correct answer.

## :warning: Why the cost of a mistake is higher in C++

In languages with managed memory, incorrect code usually fails loudly and immediately. In C++ this is not the case.

- **Undefined behavior may not show up in tests.** A data race, access to freed memory, an out-of-bounds array access — all of these can work "fine" on your machine for years and then blow up on a user's machine or after a compiler upgrade. No test guarantees that generated code is free of them.
- **Object lifetime is the trickiest spot.** This is exactly where models go wrong most often: they return a reference to a local object, capture a variable into a lambda by reference, and do not stop to think about who owns the object.
- **Concurrency.** Code that looks correct may contain a race that reproduces once a week under load.

The conclusion is simple: **you can only accept code you are able to verify**. And to verify C++ code, you need to know C++ no worse than you would when writing it by hand. The tools that help — sanitizers, static analyzers, fuzzing — are described in [Language toolkit](Tooling.md).

## :bulb: The bottleneck of development is not typing speed

This is the most important point. An engineer's job has never come down to typing characters. It consists of:

- figuring out what the customer actually needs (they usually do not get it right the first time either);
- deciding which errors in the system **must not** happen, and what to do when they happen anyway;
- trade-offs: speed versus readability, deadlines versus technical debt, reliability versus cost;
- being accountable for the result.

None of these tasks can be delegated to a model — not because it is "not smart enough," but because they are questions about people, money, and responsibility. If an application harms a user, it is the company and specific engineers who answer for it, not the tool. In fields where software is certified — medicine, avionics, automotive (see [Coding standards and regulatory requirements](Compliance.md)) — this is no longer philosophy but a literal requirement: a human signs off on the result.

Another observation, known long before neural networks: **reading someone else's code is harder than writing your own**. As there is more code and it is written faster, the bottleneck becomes not writing but understanding and reviewing. That is a job for an engineer, and its volume is more likely to grow.

## :chart_with_upwards_trend: What actually changes

It would be dishonest to say nothing is happening. Something is, and here is what is already visible:

- **Routine loses its value.** The ability to quickly write yet another boilerplate class is no longer an advantage in itself.
- **The value of verification and systems thinking grows.** The ability to notice that a proposed solution is elegant but will not hold up under load or will not fit the existing architecture becomes a key skill.
- **The entry bar has risen.** A junior was always expected to be able to write code. Now they are increasingly expected to be able to evaluate someone else's code too — including code written by a machine.

The practical takeaway: invest in the fundamentals — the memory model, object lifetime, concurrency, architecture, debugging. Everything that lets you judge whether a solution is correct. That is exactly what the [roadmap](../README.md) is about.

## :hourglass: A trap for those who are still learning

The most serious risk of AI for a beginning developer is not "it will take your job" but that it will **get in the way of learning**.

Skill grows out of wrestling with a problem: you try, you fail, you figure out why, and a mental model of what is going on stays in your head. If you ask an assistant at every difficulty, the problem gets solved but the mental model does not. After a year of practice like that, it turns out you have no way to check the assistant's answer.

What to do about it:

- On learning exercises, **solve it yourself first**, and go to the assistant for a review of a finished solution — "what could have been done better here and why."
- Ask for an explanation, not code: why this way, what the alternatives are, what breaks when the conditions change.
- Do not paste in code you cannot explain line by line. This rule works equally well for code from Stack Overflow and for code from a model.
- From time to time, write something with no assistant at all — so you can honestly see your real level.

## :handshake: How to use it usefully

- **As a routine accelerator:** boilerplate code, test scaffolding, exploring an unfamiliar API, documentation drafts.
- **As an explaining companion:** "why is the compiler complaining like this?" — models decode C++ template errors noticeably better than the compiler does.
- **As a navigator through an unfamiliar codebase:** quickly understanding where things are and how they connect.
- **As a reviewer:** ask it to find problems in your code. Not as the final word, but as one more pair of eyes.

And three rules worth keeping in mind at all times: verify what is generated, follow your company's policy on sending code to external services, and remember the licensing risks. More on this in the section on [AI tools](Tooling.md).

## :telescope: What nobody knows

Honestly: nobody knows what the profession will look like in ten years — not the authors of this roadmap, not the authors of the models themselves. Anyone who confidently predicts either "everyone will be replaced" or "nothing will change" is passing off wishful thinking as fact.

What can be said with confidence: demand for people who understand how systems work and can be accountable for the result has not gone anywhere so far. Tools in development have always changed — assembly, compilers, IDEs, autocompletion, internet search. Each time the refrain was "now anyone can program," and each time there was more work, not less, because cheaper development opened up new problems to solve. The current turn may yet prove different — but there is so far no basis for betting that deep knowledge will suddenly lose its value.

---

[**To main page**](../README.md)
