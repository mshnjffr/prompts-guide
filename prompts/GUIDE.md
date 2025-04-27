# Introduction 
Prompt engineering is a relatively new discipline for developing and optimising prompts to efficiently use language models (LMs) for a wide variety of applications and research topics.

Prompt engineering is not just about designing and developing prompts. It encompasses a wide range of skills and techniques that are useful for interacting and developing with LLMs. It's an important skill to interface, build with, and understand capabilities of LLMs.

## Basics of Prompting 
You can achieve a lot with simple prompts, but the quality of results depends on how much information you provide it and how well-crafted the prompt is. A prompt can contain information like the instruction or question you are passing to the model and include other details such as context, inputs, or examples. You can use these elements to instruct the model more effectively to improve the quality of results.

**Basic example**

Prompt
```
What is SOLID principles?
```

Output: 
```
SOLID is an acronym for five object-oriented design principles that help make software designs more understandable, flexible, and maintainable. Here's a detailed explanation of each principle:

1. S - Single Responsibility Principle (SRP):
- A class should have only one reason to change
- Each class should have only one responsibility/job
```java
// Bad Example
class UserManager {
    void saveUser() { /* ... */ }
    void sendEmail() { /* ... */ }
}

// Good Example
class UserManager {
    void saveUser() { /* ... */ }
}

class EmailService {
    void sendEmail() { /* ... */ }
}

2. O - Open/Closed Principle (OCP):
- Software entities should be open for extension but closed for modification
- You should be able to add new functionality without changing existing code

// Bad Example
class Rectangle {
    void draw() { /* ... */ }
}

// Good Example
interface Shape {
    void draw();
}

class Rectangle implements Shape {
    public void draw() { /* ... */ }
}

class Circle implements Shape {
    public void draw() { /* ... */ }
}

3. L - Liskov Substitution Principle (LSP):
- Derived classes must be substitutable for their base classes
- Objects of a superclass should be replaceable with objects of its subclasses without breaking the application

// Bad Example
class Bird {
    void fly() { /* ... */ }
}
class Penguin extends Bird { // Penguins can't fly!
    void fly() { throw new UnsupportedOperationException(); }
}

// Good Example
interface FlyingBird {
    void fly();
}
class Sparrow implements FlyingBird {
    public void fly() { /* ... */ }
}

4. I - Interface Segregation Principle (ISP):
- Clients should not be forced to depend on interfaces they don't use
- Many client-specific interfaces are better than one general-purpose interface

// Bad Example
interface Worker {
    void work();
    void eat();
    void sleep();
}

// Good Example
interface Workable {
    void work();
}
interface Eatable {
    void eat();
}
interface Sleepable {
    void sleep();
}

5. D - Dependency Inversion Principle (DIP):
- High-level modules should not depend on low-level modules. Both should depend on abstractions
- Abstractions should not depend on details. Details should depend on abstractions

// Bad Example
class EmailService {
    void sendEmail() { /* ... */ }
}
class NotificationService {
    private EmailService emailService = new EmailService();
}

// Good Example
interface MessageService {
    void sendMessage();
}
class EmailService implements MessageService {
    public void sendMessage() { /* ... */ }
}
class NotificationService {
    private MessageService messageService;
    public NotificationService(MessageService service) {
        this.messageService = service;
    }
}

Benefits of following SOLID principles:
1. Increased code maintainability
2. Better code reusability
3. More testable code
4. Reduced complexity
5. Better code organization
6. Easier to refactor
7. More flexible and scalable code

These principles work together to create more robust and maintainable software systems. While it might take more initial effort to implement them, they can save significant time and effort in the long run, especially when maintaining and extending the software.

```

Looks accurate however I was just looking for a high level overview of what SOLID was and I didn’t require the code examples so we can add more details to the prompt below

Prompt

What is SOLID principles? do not provide code examples, provide high-level, short summary

Output:
```
SOLID is an acronym for five object-oriented design principles that help create more maintainable, flexible, and scalable software:

1. Single Responsibility Principle (SRP):
- A class should have only one reason to change
- Each class should be responsible for a single piece of functionality

2. Open/Closed Principle (OCP):
- Software entities should be open for extension but closed for modification
- Add new functionality by extending rather than changing existing code

3. Liskov Substitution Principle (LSP):
- Objects of a superclass should be replaceable with objects of its subclasses
- Derived classes must be substitutable for their base classes

4. Interface Segregation Principle (ISP):
- Clients should not be forced to depend on interfaces they don't use
- Many specific interfaces are better than one general-purpose interface

5. Dependency Inversion Principle (DIP):
- High-level modules should not depend on low-level modules
- Both should depend on abstractions
- Abstractions should not depend on details

These principles aim to create more:
- Maintainable code
- Reusable code
- Flexible systems
- Testable software
- Loosely coupled components
```

Looks better. With this prompt, you are instructing the model better, and rather than making the model guess what you want. The response was exactly what I told it to do (‘do not provide code examples, provide short summary’), you can be more clear and concise on the exact response you want. 

**Prompt formatting**
A standard prompt has the following format: 
```
<Question>?
Or
<Instruction>
```


**Example Question**
What is object orientated programming? provide short summary.

**Example Output**
```
Object-Oriented Programming (OOP) is a programming paradigm that organizes code into objects, which are instances of classes. Here's a short summary:

Key concepts:
1. Classes: Templates/blueprints that define object properties and behaviors
2. Objects: Instances of classes containing data and methods
3. Encapsulation: Bundling data and methods that operate on that data within a single unit
4. Inheritance: Classes can inherit properties and methods from other classes
5. Polymorphism: Objects can take multiple forms while sharing common interfaces

Benefits:
- Reusable code
- Better organization
- Easier maintenance
- More modular structure
- Better data security through encapsulation

OOP is widely used in modern programming languages like Java, Python, C++, and C#.
```
**Example Instruction**  
Create simple python function which takes the users date of birth (DD-MM-YYYY) format and calculates their age

**Example Output**  
Here's a simple Python function that calculates age based on the user's date of birth:

```python
from datetime import datetime

def calculate_age(dob):
    try:
        # Convert string to date object
        dob = datetime.strptime(dob, "%d-%m-%Y")
        
        # Get current date
        today = datetime.today()
        
        # Calculate age
        age = today.year - dob.year
        
        # Check if birthday hasn't occurred this year
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            age -= 1
            
        return age
    
    except ValueError:
        return "Invalid date format. Please use DD-MM-YYYY"

# Example usage
if __name__ == "__main__":
    date_of_birth = input("Enter your date of birth (DD-MM-YYYY): ")
    age = calculate_age(date_of_birth)
    
    if isinstance(age, int):
        print(f"You are {age} years old")
    else:
        print(age)
```

When prompting like the above, it's also referred to as zero-shot prompting, i.e., you are directly prompting the model for a response without any examples or demonstrations about the task you want it to achieve. Some large language models have the ability to perform zero-shot prompting but it depends on the complexity and knowledge of the task at hand and the tasks the model was trained to perform good on.

## Elements of a prompt 
A prompt contains any of the following elements:

Instruction - a specific task or instruction you want the model to perform

Context - external information or additional context that can steer the model to better responses

Input Data - the input or question that we are interested to find a response for


## General tips
**Start simple**  
As you get started with designing prompts, you should keep in mind that it is really an iterative process that requires a lot of experimentation to get optimal results. You can start with simple prompts and keep adding more elements and context as you aim for better results. Iterating your prompt along the way is vital for this reason.

When you have a big task that involves many different subtasks, you can try to break down the task into simpler subtasks and keep building up as you get better results. This avoids adding too much complexity to the prompt design process at the beginning.

**Instruction**  
You can design effective prompts for various simple tasks by using commands to instruct the model what you want to achieve, such as "Write", "Classify", "Summarize", "Translate", "Order", etc.

Keep in mind that you also need to experiment a lot to see what works best. Try different instructions with different keywords, contexts, and data and see what works best for your particular use case and task. Usually, the more specific and relevant the context is to the task you are trying to perform, the better.

**Be specific**  
Be very specific about the instruction and task you want the model to perform. The more descriptive and detailed the prompt is, the better the results. This is particularly important when you have a desired outcome or style of generation you are seeking. There aren't specific tokens or keywords that lead to better results. It's more important to have a good format and descriptive prompt.

When designing prompts, you should also keep in mind the length of the prompt as there are limitations regarding how long the prompt can be. Thinking about how specific and detailed you should be. Including too many unnecessary details is not necessarily a good approach. The details should be relevant and contribute to the task at hand. This is something you will need to experiment with a lot. We encourage a lot of experimentation and iteration to optimize prompts for your applications.

## Prompting Techniques  
**Zero-shot prompting**  
Zero-shot prompting means that the prompt used to interact with the model won't contain examples or demonstrations. The zero-shot prompt directly instructs the model to perform a task without any additional examples to steer it.

**Few-shot prompting**  
While large-language models demonstrate remarkable zero-shot capabilities, they still fall short on more complex tasks when using the zero-shot setting. Few-shot prompting can be used as a technique to enable in-context learning where we provide demonstrations in the prompt to steer the model to better performance.

**Chain-of-Thought prompting**  
Chain-of-Thought (COT) is a Technique that enhances the reasoning capabilities of large language models (LLMs) by incorporating logical steps—or a “chain of thought”—within the prompt. Unlike direct-answer prompting, CoT guides the model to work through intermediate reasoning steps, making it more adept at solving complex tasks like math problems, commonsense reasoning, and symbolic manipulation.

There are many more techniques such as the following 

Role prompting 
Step-back prompting
Tree of thoughts 
Reason and Act 
Automatic prompt engineering 
Meta prompting

Probably many more! Use based on your use-cases/needs. 

