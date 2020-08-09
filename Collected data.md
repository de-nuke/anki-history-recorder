History Recorder collects various information about the learning process. For each answered card, a record is created and saved in a CSV file as well as send to the cloud. 
The record consists of 34 columns: [uid](#uid), [sid](#sid), [timestamp](#timestamp), [card_id](#card_id), [deck_id](#deck_id), [deck_name](#deck_name), [question](#question), [answer](#answer), [question_fields](#question_fields), [answer_fields](#answer_fields), [note_type](#note_type), [model_type](#model_type), [question_has_cloze](#question_has_cloze),
 [question_has_type_in](#question_has_type_in), [question_has_type_in_cloze](#question_has_type_in_cloze), [question_has_sound](#question_has_sound), [answer_has_sound](#answer_has_sound), [question_has_video](#question_has_video), [answer_has_video](#answer_has_video), [question_has_image](#question_has_image), [answer_has_image](#answer_has_image),
 [ease](#ease), [type](#type), [new_type](#new_type), [queue](#queue), [new_queue](#new_queue), [due](#due), [reps](#reps), [last_interval](#last_interval), [answered_at](answered_at), [time_taken](time_taken), [grade_time](#grade_time), [total_study_time](total_study_time), [ESTIMATED_INTERVAL](#ESTIMATED_INTERVAL) .
 
 
This document describes what type of data is collected in each column and why.
    
    
### Fields
##### `uid`
User ID. Used as one of the fields that uniquely identify a record (1/4). 

##### `sid`
Session ID. *Session* means "learning session". Each time you open Anki, new session ID is generated. It is simply random float number. This field is used as one of the fields that uniquely identify a record (2/4).

##### `timestamp` 
Moment in time when the record was created (more or less it's the moment when you rate an ease of the card). This field is used as one of the fields that uniquely identify a record (3/4).

##### `card_id` 
ID of the card. This field is used as one of the fields that uniquely identify a record (4/4).

##### `deck_id`
ID of the deck.

##### `deck_name`
Name of the deck. Might be useful in a lexical analysys to retrieve key words describing the deck.

##### `questionb`
Text of the front side of the card (question). The text is a clear text without HTML markups, images, or any elements from card template. Might be useful in a lexical analysys. If there is only image, sound or video and only template HTML, then this field is empty.

##### `answer`
Text of the back side of the card (answer). The text is a clear text without HTML markups, images, or any elements from card template. Might be useful in a lexical analysys. If there is only image, sound or video and only template HTML, then this field is empty.

##### `question_fields`
Name of the fields in the front side of the card. Might be useful in a lexical analysys to retrieve key words for the card.

##### `answer_fields`
Name of the fields in the back side of the card. Might be useful in a lexical analysys to retrieve key words for the card.

##### `note_type`
Name of the note type. Icludes both builtin types as well as custom ones, created by users. Some types like "Basic" or "Cloze" can be useful in determining if note type has an impact on learning process. 

##### `model_type`
One of two values: "STANDARD" or "CLOZE". It specifies whether it was "standard" card or had a cloze, which also may have an impact on learning efficiency. 

##### `question_has_cloze`
Whether there was a cloze on a question side o the card.

##### `question_has_type_in`
Whether there was a text input on the question side of the card.

##### `question_has_type_in_cloze`
Whetther there was cloze as a text input on the question side of the card.

##### `question_has_sound`
Whether there was a sound on the question side of the card.

##### `answer_has_sound`
Whether there was a sound on the answer side of the card.

##### `question_has_video`
Whether there was a video on the question side of the card.

##### `answer_has_video`
Whether there was a video on the answer side of the card.

##### `question_has_image`
Whether there was an image on the question side of the card.

##### `answer_has_image`
Whether there was an image on the answer side of the card.

##### `ease`
Your rated ease of the card. One of the most important factors in estimating interval. Will be also useful in a machine learning process.

##### `type`
Type of the card before an answer (before rating an ease). Might be on the values: `new`, `learning`, `review`, `relearning`.

##### `new_type`
Type of the card after an answer (after rating an ease). Might be on the values: `new`, `learning`, `review`, `relearning`.

##### `queue`
Type of the queue card was in before an answer (before rating an ease). Might be on of the values: `manually_burried`, `sibling_buried`, `suspended`, `new`, `learning`, `review`, `day_learn_relearn`, `preview`.

##### `new_queue`
Type of the queue card was in after an answer (before rating an ease). Might be on of the values: `manually_burried`, `sibling_buried`, `suspended`, `new`, `learning`, `review`, `day_learn_relearn`, `preview`.

##### `due`
When the card should be shown again. It can be a timestamp if should be shown the same day or a number of days if should be shown no sooner than the next day. Might be used to test the network - to compare network output with original Anki's algorithm.

##### `reps`
How many times the card has been already answered. Important factor in estimating interval.

##### `last_interval`
Previusly estimated interval for the card.

##### `answered_at`
Date and time of the answer. Moment of the day when user is studying might have an impact on his performance. 

##### `time_taken`
Time taken to answer the cards. Another useful information about the learning process which can have an impact on the estimated interval.

##### `grade_time`
How much time it took to rate an ease of the card. This is a meta-information about user performance. 

##### `total_study_time`
How much time has passed since the beginning of the study session. Valuable information that might correlate with user's performance.

##### `ESTIMATED_INTERVAL`
Interval before displaying the card to the user next time calculated by Anki's original algorithm. Used to measure neural network performance and to compare it with Anki. 
 
