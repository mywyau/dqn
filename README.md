# Pathfinding

## src/michael_version/ - run the following

```
python3 train_dqn.py                
```

### To test Reinforcement Learning model

```
python3 test_dqn.py                
```

### Unit tests

```
python -m unittest discover -s tests
```

Or just run the convenience scripts since you need to set the PYTHONPATH etc.

```
./run_tests.sh
```

### To train the model

```
./run_train_model.sh
```

### After training once model has been created, test in a pygame simulation

```
./run_test_model.sh
```