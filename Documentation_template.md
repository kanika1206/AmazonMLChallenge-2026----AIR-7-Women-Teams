# Business Entity Resolution: Portfolio Case Study

## Project context

Team Agastaya developed a business entity resolution solution for the Amazon ML Challenge. The original attribution lists Kanika, Kiran Sehrawat, and Mahee Agarwal. This document describes team work; the available source material does not establish individual ownership of specific components.

The task links noisy Source 2 and Source 3 business records to a deduplicated Source 1 reference. Names and addresses contain spelling differences, abbreviations, multilingual text, missing information, and ambiguous similarities. A successful system must avoid false merges while recovering genuine matches and recognizing singletons.

## High-level architecture

The full project reduced the search space through candidate generation, represented plausible pairs with similarity features, trained gradient-boosted models, incorporated additional evidence in a second learning stage, and converted scores into precision-oriented matches. It also validated output structure and identifiers.

The public edition contains selected utilities, not an end-to-end implementation. Production blocking, specialized feature engineering, second-stage evidence construction, model settings, decision policies, and production orchestration are withheld. No equivalent replacement production pipeline is provided.

## Public implementation

Retained components demonstrate explicit TSV schemas, missing-value handling, row-index and record-ID mapping, basic normalization, parallel text processing, standard string similarities, generic LightGBM wrappers, macro F0.5 computation, geographic parsing, and output-format checks. Existing generic algorithms are retained. Normalization and feature extraction are reduced only where necessary to withhold production details.

The public training wrapper accepts caller-supplied parameters. It contains no tuned model configuration, candidate ranker, or production fold/sampling policy. The output helpers serialize supplied pairs; they do not decide production matches. The utilities in `postprocess` contain no rule cascade or tuned acceptance/rejection logic.

## Evaluation methodology

Macro F0.5 is computed per reference entity and averaged across all entities, including singletons. It emphasizes precision, reflecting the cost of incorrectly merging distinct businesses. The full project used entity-based out-of-fold classifier evaluation and error analysis. This is a description of the development methodology, not a claim that every upstream learned component underwent independent nested validation.

Public tests verify basic similarities, evaluation including singletons, and output formatting on fabricated records. They do not expose the removed production behavior or benchmark a newly trained public model.

## Reported aggregate results

| System | Reported result | Interpretation |
|---|---|---|
| Historical Final submission | Public leaderboard macro F0.5 0.987026 | Historical team result |
| Private rebuilt pipeline | Out-of-fold macro F0.5 0.9792 | Development result from components withheld here |
| Private rebuilt versus historical Final | Pair Jaccard 0.9451; identical matches for 84.2% of entities | Rebuilt and historical outputs differ |
| Public utility edition | No benchmark reported | Selected runnable components, not a competition solution |
| Proposed ensemble | No achieved score reported | Experimental proposal, not a validated result |

These values are reproduced from the original project report and are not newly measured by the public edition. The original leaderboard model's complete settings and seed were not retained. The public edition does not reproduce the historical submission or the private rebuilt outputs.

## Engineering challenges and lessons

The test set involved approximately 1.73 million reference entities and 9.97 million other records. A full pairwise comparison was impractical. The project therefore focused on reducing candidate volume, controlling intermediate memory use, and processing data in chunks. The original report recorded a peak memory measurement of 25.8 GB for the full private run; this is not a public-edition resource guarantee.

Other challenges included ambiguity when addresses are missing, multilingual text variation, generalization to a country absent from training, and balancing false merges against missed links. Aggregate error analysis and careful output validation were central to development. Production-specific findings and tuned remedies are withheld.

## Data and scope

The dataset and training labels are public challenge resources and remain available in the cleaned local archive. Only operating-system metadata and explanatory comments/docstrings in the archived validator were removed from that distribution; challenge data bytes and executable validator logic are preserved. No private data or credentials were identified in the audit.

This portfolio presents selected code and engineering evidence. It contains no saved production predictions, candidate outputs, trained weights, feature matrices, probability dumps, submission archives, or recipe for reconnecting the withheld system.
