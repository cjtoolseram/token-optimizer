# Token Optimizer — Example Results

Demonstration of prompt optimization across 3 strategies: **conservative**, **moderate**, and **aggressive**.

---

## Prompt 1: AI History Summary Request

### Original (138 words)

> Please, could you kindly help me write a summary of the following text? I would really appreciate it if you could make it concise and to the point. The text is about the history of artificial intelligence, which is basically a field of computer science that focuses on creating intelligent machines that can think and learn like humans. Artificial intelligence has been around for quite a long time, actually since the 1950s, when researchers first began exploring the idea of machine intelligence. Over the years, AI has evolved significantly, going through various stages of development. In the early days, AI research focused on symbolic reasoning and problem-solving. Then, in the 1980s and 1990s, machine learning became more prominent. More recently, deep learning has revolutionized the field, enabling breakthroughs in areas like natural language processing, computer vision, and robotics.

### Conservative (138 words, 0% saved)

> Please, could you kindly help me write a summary of the following text? I would really appreciate it if you could make it concise and to the point. The text is about the history of artificial intelligence, which is basically a field of computer science that focuses on creating intelligent machines that can think and learn like humans. Artificial intelligence has been around for quite a long time, actually since the 1950s, when researchers first began exploring the idea of machine intelligence. Over the years, AI has evolved significantly, going through various stages of development. In the early days, AI research focused on symbolic reasoning and problem-solving. Then, in the 1980s and 1990s, machine learning became more prominent. More recently, deep learning has revolutionized the field, enabling breakthroughs in areas like natural language processing, computer vision, and robotics.

### Moderate (132 words, 4% saved)

> , could you help me write summary of the following text? I would appreciate it if you could make it concise and to the point. The text is about the history of artificial intelligence, which is a field of computer science that focuses on creating intelligent machines that can think and learn like humans. Artificial intelligence has been around for a long time, since the 1950s, when researchers first began exploring the idea of machine intelligence. Over the years, AI has evolved significantly, going through various stages of development. In the early days, AI research focused on symbolic reasoning and problem-solving. Then, in the 1980s and 1990s, machine learning became more prominent. More recently, deep learning has revolutionized the field, enabling breakthroughs in areas like natural language processing, computer vision, and robotics.

### Aggressive (132 words, 4% saved)

> , could you help me write summary of the following text? I would appreciate it if you could make it concise and to the point. The text is about the history of artificial intelligence, which is a field of computer science that focuses on creating intelligent machines that can think and learn like humans. Artificial intelligence has been around for a long time, since the 1950s, when researchers first began exploring the idea of machine intelligence. Over the years, AI has evolved significantly, going through various stages of development. In the early days, AI research focused on symbolic reasoning and problem-solving. Then, in the 1980s and 1990s, machine learning became more prominent. More recently, deep learning has revolutionized the field, enabling breakthroughs in areas like natural language processing, computer vision, and robotics.

---

## Prompt 2: Translation Task

### Original (92 words)

> I want you to act as a professional translator. I would really appreciate it if you could please translate the following paragraph from English to a more formal and professional tone. Please make sure to keep the original meaning intact. Please do not add any additional information. Here is the text: Our team has been working very hard on this project for the past few months. We have made significant progress and we are very excited about the results. We believe that this project will have a major impact on the industry.

### Conservative (88 words, 4% saved)

> act as a professional translator. I would really appreciate it if you could please translate the following paragraph from English to a more formal and professional tone. Please make sure to keep the original meaning intact. Please do not add any additional information. Here is the text: Our team has been working very hard on this project for the past few months. We have made significant progress and we are very excited about the results. We believe that this project will have a major impact on the industry.

### Moderate (82 words, 10% saved)

> act as a professional translator. I would appreciate it if you could translate the following paragraph from English to a more formal and professional tone. make sure to keep the original meaning intact. do not add any additional information. Here is the text: Our team has been working hard on this project for the past few months. We have made significant progress and we are excited about the results. We believe that this project will have a major impact on the industry.

### Aggressive (82 words, 10% saved)

> act as a professional translator. I would appreciate it if you could translate the following paragraph from English to a more formal and professional tone. make sure to keep the original meaning intact. do not add any additional information. Here is the text: Our team has been working hard on this project for the past few months. We have made significant progress and we are excited about the results. We believe that this project will have a major impact on the industry.

---

## Prompt 3: Cooking Assistant System Prompt

### Original (70 words)

> You are a helpful assistant that helps people with cooking. You should always be polite and friendly. You should provide detailed step-by-step instructions. You should also mention any potential allergens. You should suggest substitutions for common ingredients when possible. Now, please tell me how to make a simple pasta dish with tomato sauce. I would like it to be vegetarian. Please include the list of ingredients and the cooking time.

### Conservative (70 words, 0% saved)

> You are a helpful assistant that helps people with cooking. You should always be polite and friendly. You should provide detailed step-by-step instructions. You should also mention any potential allergens. You should suggest substitutions for common ingredients when possible. Now, please tell me how to make a simple pasta dish with tomato sauce. I would like it to be vegetarian. Please include the list of ingredients and the cooking time.

### Moderate (67 words, 4% saved)

> You are a helpful assistant that helps people with cooking. You should always be polite and friendly. You should provide detailed step-by-step instructions. You should also mention any potential allergens. You should suggest substitutions for common ingredients when possible. Now, tell me how to make simple pasta dish with tomato sauce. I would like it to be vegetarian. include the list of ingredients and the cooking time.

### Aggressive (59 words, 14% saved)

> You are a helpful assistant that helps people with cooking. always be polite and friendly. provide detailed step-by-step instructions. also mention any potential allergens. suggest substitutions for common ingredients when possible. Now, tell me how to make simple pasta dish with tomato sauce. I would like it to be vegetarian. include the list of ingredients and the cooking time.

---

## Summary

| Prompt | Original | Conservative | Moderate | Aggressive |
|--------|----------|--------------|----------|------------|
| AI History Summary | 138 words | 138 words (0%) | 132 words (-4%) | 132 words (-4%) |
| Translation Task | 92 words | 88 words (-4%) | 82 words (-10%) | 82 words (-10%) |
| Cooking Assistant | 70 words | 70 words (0%) | 67 words (-4%) | 59 words (-14%) |

### What gets removed

- **Conservative**: "I want you to" preambles
- **Moderate**: + filler words ("really", "very", "kindly", "basically"), redundant "please"
- **Aggressive**: + "You should" repetitions, unnecessary articles, polite openers

### Testing recommendation

Copy the **original** and **aggressive** versions of each prompt and send them to GPT-4, Claude, or Gemini. The LLM output should be functionally identical, confirming that semantic meaning is preserved while tokens are saved.
