**Meeting notes from the first meeting**

*Description & concept*

- The idea is functional and something that we can execute for this course
- The description of the concept is okay but the diagram needs improvements. For example the relations between concepts should be drawn more precisely.
- Gym workouts with movements and user favorites are considered to be enough as the scope of this project

*Use cases*

- The initial use cases are out of scope because they are describing the persons using them rather than the apps using the API.
- We should add a second client that is algorithmic so it fetches data from the API and aggregates it somehow

*Related work*

- Nothing to correct there

**Meeting notes from the second meeting**

*Database tables*

- User names should be unique, otherwise okay

*Database implementation*

- BMI should be declared as property so it can be used like 'user.bmi'
- on_delete behavior for foreign keys should be implemented
- The installation of requirements does not work properly, needs to be fixed (the command was pip freeze, that only creates the file)
- We forgot to commit our latest changes for the github so need to fix that before the next meeting

**Meeting minutes from third meeting**

*Implementation*

- Tests should be at root in their own folder
- Could explain more about details of resources methods and what Pylint tests should return
- Coverage looks very good

*About the previous parts:*

- Lacking the service description in API uses

