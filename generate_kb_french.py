import os
from pathlib import Path

# Создаем директорию для базы знаний
kb_dir = Path("french_kb")
kb_dir.mkdir(exist_ok=True)

# Словарь с названиями файлов и их содержимым
documents = {
    "01_prononciation_et_liaison.md": """# Правила произношения и связывания (Liaison)

## 1. Основы французской фонетики
- Французский язык имеет фиксированное ударение: оно всегда падает на последний произносимый слог слова или группы слов.
- Конечные согласные (d, s, t, x, z, p) обычно не произносятся, кроме c, r, f, l (правило "CaReFuL").

## 2. Связывание (Liaison)
Liaison — это произнесение конечной согласной перед словом, начинающимся с гласной или немого h.
- **Обязательная связка**: после артиклей (les amis [lezami]), местоимений (nous avons [nuzavon]), коротких предлогов (en été [ɑ̃nete]).
- **Запрещенная связка**: после "et" (и), перед гортанной h (les haricots), после существительного в единственном числе.

## 3. Enchaînement
В отличие от liaison, enchaînement — это связывание согласной, которая является частью того же слова (например, "elle est" [ɛlɛ]).
""",

    "02_articles_et_genres.md": """# Артикли и род существительных

## 1. Определенные артикли (le, la, l', les)
Используются для обозначения конкретных предметов или общих понятий.
- le (м.р., перед согласной): le livre
- la (ж.р., перед согласной): la table
- l' (перед гласной или немым h): l'homme, l'école
- les (мн.ч.): les livres, les tables

## 2. Неопределенные артикли (un, une, des)
- un (м.р.): un stylo
- une (ж.р.): une pomme
- des (мн.ч.): des pommes

## 3. Частичный артикль (du, de la, de l', des)
Используется с неисчисляемыми существительными (еда, напитки, абстрактные понятия).
- Je mange du pain. Je bois de l'eau.

## 4. Определение рода
- М.р. часто оканчиваются на: -age, -ment, -eau, -isme.
- Ж.р. часто оканчиваются на: -tion, -sion, -té, -ette, -ance, -ence.
""",

    "03_veres_reguliers_present.md": """# Спряжение правильных глаголов в настоящем времени (Présent)

## 1. Глаголы первой группы (-er)
Пример: PARLER (говорить)
- je parl**e**
- tu parl**es**
- il/elle/on parl**e**
- nous parl**ons**
- vous parl**ez**
- ils/elles parl**ent**
*Исключение*: aller (неправильный).

## 2. Глаголы второй группы (-ir, с суффиксом -iss-)
Пример: FINIR (заканчивать)
- je fin**is**
- tu fin**is**
- il/elle/on fin**it**
- nous fin**issons**
- vous fin**issez**
- ils/elles fin**issent**

## 3. Глаголы третьей группы (разноспрягаемые, -re, -oir, некоторые -ir)
Требуют индивидуального запоминания. Примеры: prendre, mettre, voir, pouvoir.
""",

    "04_veres_irreguliers_essentiels.md": """# Ключевые неправильные глаголы (Présent)

## 1. Être (быть)
je suis, tu es, il est, nous sommes, vous êtes, ils sont.

## 2. Avoir (иметь)
j'ai, tu as, il a, nous avons, vous avez, ils ont.

## 3. Aller (идти)
je vais, tu vas, il va, nous allons, vous allez, ils vont.

## 4. Faire (делать)
je fais, tu fais, il fait, nous faisons, vous faites, ils font.

## 5. Модальные глаголы
- Pouvoir (мочь): je peux, tu peux, il peut, nous pouvons, vous pouvez, ils peuvent.
- Vouloir (хотеть): je veux, tu veux, il veut, nous voulons, vous voulez, ils veulent.
- Devoir (долженствовать): je dois, tu dois, il doit, nous devons, vous devez, ils doivent.
""",

    "05_passe_compose_vs_imparfait.md": """# Прошедшие времена: Passé Composé и Imparfait

## 1. Passé Composé (Завершенное действие)
Используется для конкретных, завершенных действий в прошлом, которые прерывают течение времени или являются фактом.
- **Образование**: вспомогательный глагол (avoir или être) в présent + participe passé.
- *Пример*: Hier, j'ai mangé une pomme. (Вчера я съел яблоко).

## 2. Imparfait (Незавершенное, фоновое действие)
Используется для описания состояния, привычек, фоновых действий или одновременных процессов в прошлом.
- **Образование**: основа nous из présent + окончания: -ais, -ais, -ait, -ions, -iez, -aient.
- *Пример*: Quand j'étais petit, je jouais au foot. (Когда я был маленьким, я играл в футбол).

## 3. Ключевые маркеры
- Passé Composé: hier, soudain, une fois, tout à coup.
- Imparfait: souvent, toujours, chaque jour, pendant que.
""",

    "06_pronoms_cod_coi.md": """# Местоимения: прямое и косвенное дополнение (COD и COI)

## 1. Прямое дополнение (COD)
Отвечает на вопросы "qui ?" или "quoi ?". Заменяет существительное без предлога.
- me, te, le/la, nous, vous, les.
- *Пример*: Je vois le chat -> Je **le** vois.

## 2. Косвенное дополнение (COI)
Отвечает на вопрос "à qui ?". Заменяет одушевленное существительное с предлогом "à".
- me, te, lui, nous, vous, leur.
- *Пример*: Je parle à Marie -> Je **lui** parle.

## 3. Местоимения Y и EN
- **Y**: заменяет место или дополнение с предлогом "à" (неодушевленное). *Je vais à Paris -> J'y vais.*
- **EN**: заменяет количество или дополнение с предлогом "de". *J'ai des pommes -> J'en ai.*

## 4. Порядок местоимений перед глаголом
(Me, te, se, nous, vous) -> (le, la, les) -> (lui, leur) -> y -> en -> verbe.
*Пример*: Il me le donne. (Он дает это мне).
""",

    "07_subjonctif.md": """# Сослагательное наклонение (Le Subjonctif)

## 1. Когда используется
Выражает сомнение, желание, необходимость, эмоцию или возможность. Всегда стоит в придаточном предложении после "que".
- Триггеры: il faut que, je veux que, bien que, pour que, je doute que.

## 2. Образование (Présent du subjonctif)
Основа берется от формы "ils" в présent, плюс окончания: -e, -es, -e, -ions, -iez, -ent.
- Parler: que je parle, que nous parlions.
- Finir: que je finisse, que nous finissions.

## 3. Важные исключения
- Être: que je sois, que tu sois, qu'il soit, que nous soyons, que vous soyez, qu'ils soient.
- Avoir: que j'aie, que tu aies, qu'il ait, que nous ayons, que vous ayez, qu'ils aient.
- Faire: que je fasse.
- Aller: que j'aille.
""",

    "08_pronoms_relatifs.md": """# Относительные местоимения (Pronoms relatifs)

## 1. Qui
Заменяет подлежащее (кто/который). После qui всегда идет глагол.
- *L'homme qui parle est mon père.*

## 2. Que (qu')
Заменяет прямое дополнение (которого/которую). После que всегда идет подлежащее.
- *Le livre que je lis est intéressant.*

## 3. Dont
Заменяет дополнение с предлогом "de" (о котором, чей).
- *Le film dont je te parle est génial.* (Le film DE lequel je te parle).
- *C'est l'homme dont je connais la femme.* (Чью жену я знаю).

## 4. Où
Заменяет обстоятельство места или времени (где, когда).
- *La ville où j'habite.* / *Le jour où nous nous sommes rencontrés.*

## 5. Lequel, laquelle, lesquels, lesquelles
Используются после предлогов (sur, avec, pour, sans), кроме "de" (там используется dont).
- *La table sur laquelle je travaille.*
""",

    "09_negation.md": """# Структуры отрицания (La Négation)

## 1. Базовое отрицание
Ne + глагол + pas.
- *Je ne sais pas.* (В разговорной речи "ne" часто опускается: *Je sais pas*).

## 2. Отрицательные наречия (вместо pas)
- Ne ... jamais (никогда): *Je ne fume jamais.*
- Ne ... plus (больше не): *Il ne travaille plus ici.*
- Ne ... rien (ничего): *Je ne vois rien.*
- Ne ... personne (никого): *Je ne connais personne.*
- Ne ... que (только, лишь): *Je n'ai qu'un frère.* (У меня только один брат).

## 3. Отрицание с инфинитивом
Обе части отрицания ставятся ПЕРЕД инфинитивом.
- *Il décide de ne pas venir.* (НЕ: de ne venir pas).

## 4. Отрицание с местоимениями
Ne + местоимение + глагол + pas.
- *Je ne le sais pas.*
""",

    "10_connecteurs_logiques.md": """# Логические связки для чтения статей и эссе

## 1. Противопоставление (Opposition)
- Mais (но), cependant (однако), pourtant (тем не менее), en revanche (напротив), au contraire (наоборот), bien que + subjonctif (хотя).

## 2. Причина (Cause)
- Parce que, car (так как), puisque (поскольку), en raison de + существительное (ввиду).

## 3. Следствие (Conséquence)
- Donc (поэтому), alors (итак), par conséquent (следовательно), c'est pourquoi (вот почему), si bien que (так что).

## 4. Добавление и переход (Addition et Transition)
- Et (и), de plus (кроме того), en outre (сверх того), d'abord (сначала), ensuite (затем), enfin (наконец).

> **Совет для чтения**: Эти слова являются "якорями" текста. При анализе новости сначала найдите их, чтобы понять структуру аргументации автора.
""",

    "11_temps_litteraires.md": """# Литературные времена для чтения книг

## 1. Passé Simple (Простое прошедшее)
Используется исключительно в письменной речи (романы, исторические тексты) для обозначения завершенных действий, аналогично Passé Composé.
- 1-я группа (-er): je parlai, tu parlas, il parla, nous parlâmes, vous parlâtes, ils parlèrent.
- 2-я группа (-ir): je finis, tu finis, il finit, nous finîmes, vous finîtes, ils finirent.
- Être: je fus, tu fus, il fut, nous fûmes, vous fûtes, ils furent.
- Avoir: j'eus, tu eus, il eut, nous eûmes, vous eûtes, ils eurent.

## 2. Plus-que-parfait (Предпрошедшее время)
Действие, произошедшее до другого действия в прошлом.
- Образование: Imparfait вспомогательного глагола + participe passé.
- *Quand je suis arrivé, il était déjà parti.* (Когда я прибыл, он уже ушел).

## 3. Passé Antérieur
Литературный аналог Plus-que-parfait, используется после союзов времени (quand, lorsque, dès que, après que).
- *Dès qu'il eut fini, il sortit.*
""",

    "12_faux_amis_anglais.md": """# Ложные друзья переводчика (Faux Amis) для англоговорящих

Слова, которые выглядят как английские, но имеют другое значение:

1. **Actuellement** = в настоящее время (НЕ actually / на самом деле). *Actually* по-французски: *en fait*.
2. **Attendre** = ждать (НЕ to attend / посещать). *Посещать* = *assister à*.
3. **Blessé** = раненый (НЕ blessed / благословенный).
4. **Coin** = угол (НЕ coin / монета). *Монета* = *pièce*.
5. **Demander** = спрашивать (НЕ to demand / требовать). *Требовать* = *exiger*.
6. **Librairie** = книжный магазин (НЕ library / библиотека). *Библиотека* = *bibliothèque*.
7. **Monnaie** = мелочь, сдача (НЕ money / деньги в целом). *Деньги* = *argent*.
8. **Rester** = оставаться (НЕ to rest / отдыхать). *Отдыхать* = *se reposer*.
9. **Salade** = салат (НЕ salad / в переносном смысле "каша в голове" - это *bordel* или *pagaille*).
10. **Supporter** = терпеть, выносить (НЕ to support / поддерживать). *Поддерживать* = *soutenir*.
""",

    "13_lecture_article_modele.md": """# Пример разбора новостной статьи (Lecture et Analyse)

## Текст (Le Monde, выдержка)
"Le gouvernement a annoncé hier de nouvelles mesures économiques. Cependant, les syndicats restent sceptiques quant à leur efficacité. Ils exigent une augmentation immédiate des salaires."

## Словарный запас (Vocabulaire)
- **annoncer** (v.) : объявлять
- **les mesures** (n.f.pl) : меры
- **cependant** (adv.) : однако (логическая связка противопоставления)
- **les syndicats** (n.m.pl) : профсоюзы
- **sceptique** (adj.) : скептически настроенный
- **quant à** (loc. prép.) : что касается
- **exiger** (v.) : требовать

## Грамматический разбор
1. "a annoncé" : Passé Composé (завершенное действие в прошлом, факт).
2. "restent" : Présent (текущее состояние, фоновая ситуация).
3. "leur efficacité" : притяжательное прилагательное "leur" (их), согласуется с существительным в ед.ч.

## Вопросы для самопроверки
1. Что объявило правительство?
2. Какова реакция профсоюзов и какое слово-связка указывает на противопоставление?
""",

    "14_formation_des_questions.md": """# Формирование вопросов (L'Interrogation)

## 1. Интонация (Разговорный стиль)
Порядок слов как в утверждении, но с повышением тона в конце.
- *Tu parles français ?*

## 2. С использованием "Est-ce que" (Нейтральный стиль)
Добавляется в начало предложения, порядок слов не меняется.
- *Est-ce que tu parles français ?*

## 3. Инверсия (Формальный/Письменный стиль)
Глагол и подлежащее-местоимение меняются местами и соединяются дефисом.
- *Parles-tu français ?*
- Если глагол оканчивается на гласную, а местоимение начинается на гласную (il, elle, on), добавляется "-t-" для благозвучия: *Aime-t-il le chocolat ?*

## 4. Вопросительные слова
- **Qui** (кто), **Que / Quoi** (что), **Où** (где), **Quand** (когда), **Comment** (как), **Pourquoi** (почему), **Combien** (сколько).
- *Pourquoi est-ce que tu apprends le français ?* / *Pourquoi apprends-tu le français ?*
""",

    "15_tutor_rules_and_persona.md": """# ИНСТРУКЦИЯ ДЛЯ АССИСТЕНТА (Системные правила)

## 1. Роль
Ты — «Универсальный Лингвистический Тьютор». Твоя цель — помогать пользователю изучать французский язык, опираясь СТРОГО на предоставленную базу знаний.

## 2. Правила поведения
- **Никаких галлюцинаций**: Если правило, слово или исключение не описано в базе знаний, честно скажи: "В предоставленных материалах это правило не детализировано, но в общем случае во французском языке..."
- **Структурированность**: Всегда используй заголовки, жирный шрифт и списки для объяснения грамматики.
- **Контекст чтения**: Поскольку пользователь увлекается чтением, всегда приводи примеры из литературного или новостного контекста, а не только бытовые фразы.
- **Разбор ошибок**: Если пользователь делает ошибку, сначала похвали за попытку, затем укажи на ошибку, объясни правило (со ссылкой на документ из БЗ) и попроси исправить.

## 3. Формат генерации упражнений
Если пользователь просит упражнение, сгенерируй ровно 5 заданий:
1. Перевод с русского на французский.
2. Вставка пропущенного слова (Fill-in-the-blank).
3. Выбор правильного варианта (Multiple choice).
4. Преобразование предложения (например, в отрицание или вопрос).
5. Поиск ошибки в предложенном предложении.
Всегда предоставляй ключи с ответами в скрытом виде (или после просьбы пользователя).
"""
}

# Запись файлов на диск
for filename, content in documents.items():
    file_path = kb_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ Успешно создано {len(documents)} документов в папке '{kb_dir}'")
print("База знаний готова к загрузке в RAG (LlamaIndex / LangChain)!")
