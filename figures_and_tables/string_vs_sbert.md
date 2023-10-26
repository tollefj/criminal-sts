| Data    | CSIQ                                             | String match       | Query SBERT              | Result String | Result SBERT |
| ------- | ----------------------------------------------- | ------------------- | ------------------------ | ------------- | ------------ |
| Lovdata | Who had access to the house?                   | house               | access to the house     | 7             | 25           |
| Lovdata | What is the cause of death?                    | cause of death      | the cause of death      | 9             | 20           |
| Case A  | Who has a black van?                           | black van           | black van               | 21            | >50          |
| Case A  | Has the deceased been involved in any conflict? | conflict with <NAME> | conflict with <NAME>   | 1             | 27           |
| Case B  | Who had access to the weapon?                 | access to weapon    | access to weapon        | 25            | 47           |
| Case B  | What rumors exist about what happened?        | rumors about        | rumors about what happened | 29            | >50          |
