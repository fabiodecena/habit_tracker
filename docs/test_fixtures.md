# Test Fixture Data Specification

This document describes the predefined tracking data (test fixtures) for the 5 seeded habits over a 4-week period (exactly 28 days).

## Overview

- **Period**:   Exactly 28 days (4 weeks) from current date backward
- **Date Range**: `start_date = now() - 27 days` to `end_date = now()` (inclusive)
- **Purpose**: Consistent, predictable data for testing analytics and streak calculations
- **Habits**: 5 predefined habits with different tracking patterns
- **Status**: 4 active habits + 1 inactive habit (for testing archive functionality)

---

## Habit 1: Read Journal (Daily) ✅ ACTIVE

**Pattern**: Perfect completion streak - most disciplined habit

**Status**: ✅ **ACTIVE**

| Week | Days | Completions | Notes |
|------|------|-------------|-------|
| Week 1 | 1-7 | 7/7 | All days completed |
| Week 2 | 8-14 | 7/7 | All days completed |
| Week 3 | 15-21 | 7/7 | All days completed |
| Week 4 | 22-28 | 7/7 | All days completed |

**Total**:  28/28 completions  
**Longest Streak**: 28 days  
**Current Streak**: 28 days  
**Success Rate**: 100%

**Notes Pattern**:  Alternates between "Morning reading session" (odd days) and "Evening reading session" (even days)

**Use Case**: 
- ✅ Test perfect streak calculation
- ✅ Validate daily habit tracking with 100% completion
- ✅ Champion habit identification
- ✅ Baseline for comparison with other habits

---

## Habit 2: Skin Care (Daily) ❌ INACTIVE

**Pattern**:  Tracked for 3 weeks (21 days) with 2 missed days, then archived

**Status**: ❌ **INACTIVE** (Archived after week 3)

| Week | Days | Completions | Details |
|------|------|-------------|---------|
| Week 1 | 1-7 | 7/7 | Days 1-7 all completed |
| Week 2 | 8-14 | 5/7 | Days 10, 11 missed (busy weekend) |
| Week 3 | 15-21 | 7/7 | Days 15-21 all completed |
| Week 4 | 22-28 | - | **Not tracked (archived)** |

**Total**: 19/21 completions (only tracked for 3 weeks)  
**Longest Streak**: 11 days (days 12-21 after week 2 break, plus 1 day from week 4)  
**Current Streak**:  0 (archived)  
**Success Rate**: 90. 5% (while active)

**Completion Breakdown:**
- Days completed: 1, 2, 3, 4, 5, 6, 7, 8, 9, ~~10~~, ~~11~~, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
- Days 10-11: Missed (busy weekend)
- Days 22-28: Not tracked (habit archived)

**Notes Pattern**:  "Full routine completed" every 3rd day, otherwise "Morning routine"

**Use Case**: 
- ✅ Test that inactive habits are hidden from active lists
- ✅ Test that inactive habits appear in "List all habits (including inactive)"
- ✅ Test that inactive habits retain their historical data (19 events preserved)
- ✅ Test that archived habits can be reactivated via edit
- ✅ Test that inactive habits cannot be checked off
- ✅ Test status indicator in UI (strikethrough, dim styling)
- ✅ Test soft delete functionality

---

## Habit 3: Play Music (Daily) ✅ ACTIVE

**Pattern**: Practice schedule with regular rest days (every 5th day off)

**Status**: ✅ **ACTIVE**

| Week | Days | Completions | Rest Days |
|------|------|-------------|-----------|
| Week 1 | 1-7 | 6/7 | Day 5 (rest) |
| Week 2 | 8-14 | 5/7 | Days 10, 15 (rest) |
| Week 3 | 15-21 | 6/7 | Day 20 (rest) |
| Week 4 | 22-28 | 5/7 | Day 25 (rest) |

**Total**: 22/28 completions  
**Longest Streak**: 4 days (maximum between rest days)  
**Current Streak**: 3 days (depends on current date)  
**Success Rate**: 78.6%

**Rest Day Pattern**:  Every 5th day (days 5, 10, 15, 20, 25)

**Completion Timeline**:  ✅✅✅✅❌✅✅ | ✅✅❌✅✅✅✅ | ❌✅✅✅✅❌✅ | ✅✅✅❌✅✅✅

**Notes Pattern**:  Rotates through: 
- "Piano practice"
- "Guitar session"
- "Vocal exercises"
- "Music theory"

**Use Case**: 
- ✅ Test multiple short streaks with regular gaps
- ✅ Validate realistic practice schedule with intentional rest
- ✅ Test streak calculation with consistent pattern

---

## Habit 4: Finance Check (Weekly) ✅ ACTIVE

**Pattern**:  Perfect weekly completion (every Sunday) - consistent financial discipline

**Status**: ✅ **ACTIVE**

| Week | Completion Day | Status |
|------|----------------|--------|
| Week 1 | Sunday | ✅ Completed |
| Week 2 | Sunday | ✅ Completed |
| Week 3 | Sunday | ✅ Completed |
| Week 4 | Sunday | ✅ Completed |

**Total**: 4/4 completions  
**Longest Streak**: 4 weeks  
**Current Streak**: 4 weeks  
**Success Rate**: 100%

**Completion Pattern**: Every Sunday

**Notes Pattern**:  Rotates through different financial tasks:
- Week 1: "Budget review and expense tracking"
- Week 2: "Investment portfolio check"
- Week 3: "Bill payments verified"
- Week 4: "Savings goals updated"

**Use Case**: 
- ✅ Test weekly habit tracking
- ✅ Validate week normalization logic (all dates normalized to Monday)
- ✅ Test perfect weekly streak
- ✅ Test consistency with specific day of week

---

## Habit 5: Water Plants (Weekly) ✅ ACTIVE

**Pattern**:  Missed week 2 (broken weekly streak - was traveling)

**Status**: ✅ **ACTIVE**

| Week | Completion Day | Status |
|------|----------------|--------|
| Week 1 | Saturday | ✅ Completed |
| Week 2 | - | ❌ Missed (traveling) |
| Week 3 | Saturday | ✅ Completed |
| Week 4 | Saturday | ✅ Completed |

**Total**: 3/4 completions  
**Longest Streak**: 2 weeks (weeks 3-4)  
**Current Streak**: 2 weeks (weeks 3-4)  
**Success Rate**: 75%

**Completion Pattern**:  Every Saturday (when completed)

**Notes Pattern**:  Detailed plant care notes:
- Week 1: "Watered all plants, checked for pests"
- Week 2: *Missed*
- Week 3: "Deep watering session, trimmed dead leaves"
- Week 4: "Regular watering, soil looks healthy"

**Use Case**: 
- ✅ Test weekly streak breaks
- ✅ Validate weekly habit with single missed week
- ✅ Test current streak recovery after break
- ✅ Test different weekly day (Saturday vs Finance's Sunday)

---

## Summary Statistics

### Overall Metrics

| Metric | Value |
|--------|-------|
| **Total Habits** | 5 |
| **Active Habits** | 4 |
| **Inactive Habits** | 1 (Skin Care) |
| **Daily Habits** | 3 (Read Journal, Skin Care, Play Music) |
| **Weekly Habits** | 2 (Finance Check, Water Plants) |
| **Perfect Completion** | 2 habits (Read Journal, Finance Check) |

### Active Habits Summary

| Habit | Type | Completions | Longest Streak | Success Rate | Status |
|-------|------|-------------|----------------|--------------|--------|
| Read Journal | Daily | 28/28 | 28 days | 100% | Active |
| Play Music | Daily | 22/28 | 4 days | 78.6% | Active |
| Finance Check | Weekly | 4/4 | 4 weeks | 100% | Active |
| Water Plants | Weekly | 3/4 | 2 weeks | 75% | Active |

### Inactive Habits Summary

| Habit | Type | Completions | Longest Streak | Success Rate | Status |
|-------|------|-------------|----------------|--------------|--------|
| Skin Care | Daily | 19/21 | 11 days | 90.5% | Inactive |

---

## Testing Scenarios Covered

### ✅ Streak Calculations

| Scenario | Habit | Expected Result |
|----------|-------|-----------------|
| Perfect daily streak | Read Journal | 28 days |
| Broken daily streak | Skin Care | 11 days (longest before archiving) |
| Multiple short streaks | Play Music | 4 days (max between rest days) |
| Perfect weekly streak | Finance Check | 4 weeks |
| Broken weekly streak | Water Plants | 2 weeks (recovery after miss) |

### ✅ Analytics Functions (Functional Programming)

**1. List all tracked habits**
- Active only:  Returns 4 habits (excludes Skin Care)
- Include inactive: Returns all 5 habits
- Functional: Uses `map()`, `filter()`, `sorted()`

**2. List habits by periodicity**
- Daily active: 2 habits (Read Journal, Play Music)
- Weekly active: 2 habits (Finance Check, Water Plants)
- Daily all: 3 habits (includes inactive Skin Care)
- Functional: Uses `filter()` with lambda

**3. Longest streak of all habits**
- Champion: Read Journal (28 days)
- Functional: List comprehension + `max()` with key function

**4. Longest streak for specific habit**
- Each habit has known expected value
- Functional: Set comprehension for date normalization

### ✅ Status & Archive Testing

| Test | Expected Behavior |
|------|-------------------|
| Active habits appear in default lists | ✅ 4 habits shown |
| Inactive habit hidden from active lists | ❌ Skin Care not shown |
| Inactive habit appears when including inactive | ✅ Skin Care shown with "Archived" status |
| Inactive habit retains all historical data | ✅ 19 completions preserved |
| Status indicators in UI | ✅ Active (green) vs Archived (red, strikethrough) |
| Inactive habit cannot be checked off | ❌ Error:  "Habit is inactive" |
| Inactive habit can be reactivated | ✅ Via edit feature |

### ✅ Success Rates

| Success Rate | Habits |
|--------------|--------|
| 100% | Read Journal (28/28), Finance Check (4/4) |
| 90.5% | Skin Care (19/21) - inactive |
| 78.6% | Play Music (22/28) |
| 75% | Water Plants (3/4) |

### ✅ Edge Cases

| Edge Case | Covered By |
|-----------|------------|
| Consecutive missed days | Skin Care (days 10-11) |
| Regular pattern with gaps | Play Music (every 5th day) |
| Single week missed | Water Plants (week 2) |
| Different weekly days | Finance (Sunday) vs Water Plants (Saturday) |
| Partial period tracking | Skin Care (3 weeks before archiving) |
| Perfect completion | Read Journal, Finance Check |

---

## Expected UI Display

### When Listing Active Habits Only (Menu Option 5)

```
📋 Currently tracked habits:  

╭─────┬────────────────────┬──────────────┬──────────────────────────────────────────────╮
│     │    Habit Name      │ Periodicity  │                 Description                  │
├─────┼────────────────────┼──────────────┼──────────────────────────────────────────────┤
│ 🕐  │ Read Journal       │    Daily     │ Read a journal (20-35 minutes)               │
│ 🕐  │ Play Music         │    Daily     │ Practice an instrument for 15-30 minutes     │
│ 📆  │ Finance Check      │   Weekly     │ Review spending and update budget/accounts   │
│ 📆  │ Water Plants       │   Weekly     │ Water plants and check soil moisture/leaves  │
╰─────┴────────────────────┴──────────────┴──────────────────────────────────────────────╯

Total: 4 active habits
```

### When Listing All Habits Including Inactive (Menu Option 6)

```
📚 All habits (including inactive):

╭─────┬────────────────────┬──────────────┬──────────┬──────────────────────────────────────╮
│     │    Habit Name      │ Periodicity  │  Status  │            Description               │
├─────┼────────────────────┼──────────────┼──────────┼──────────────────────────────────────┤
│ 🕐  │ Read Journal       │    Daily     │  Active  │ Read a journal (20-35 minutes)       │
│ 🕐  │ Skin Care          │    Daily     │ Archived │ Complete your skincare routine       │
│ 🕐  │ Play Music         │    Daily     │  Active  │ Practice instrument 15-30 minutes    │
│ 📆  │ Finance Check      │   Weekly     │  Active  │ Review budget/accounts               │
│ 📆  │ Water Plants       │   Weekly     │  Active  │ Water plants and check soil          │
╰─────┴────────────────────┴──────────────┴──────────┴──────────────────────────────────────╯

Total: 5 habits (4 active, 1 archived)

Note: Archived habits appear with strikethrough styling
```

---

## Expected Analytics Results

### Champion Habit Analysis

```
🏆 Champion Habit (Longest Streak): Read Journal (28 days)

All Active Habits Ranked by Longest Streak:
1. Read Journal - 28 days (daily, 100% completion)
2. Finance Check - 4 weeks (weekly, 100% completion)
3. Play Music - 4 days (daily, 79% completion)
4. Water Plants - 2 weeks (weekly, 75% completion)

Note: Skin Care (inactive) had 11-day streak before archiving
```

### Daily vs Weekly Habits

```
🕐 Daily Habits (2 active, 1 inactive):

Active: 
- Read Journal:  28 day streak, 28/28 completions (100%)
- Play Music: 4 day streak, 22/28 completions (79%)

Archived:
- Skin Care: 11 day streak, 19/21 completions (90.5%) - INACTIVE

📆 Weekly Habits (2 active):

- Finance Check: 4 week streak, 4/4 completions (100%)
- Water Plants: 2 week streak, 3/4 completions (75%)
```

---

## Completion Timeline Visualization

### Daily Habits (28-day period)

**Read Journal** (Perfect):  
`✅✅✅✅✅✅✅ | ✅✅✅✅✅✅✅ | ✅✅✅✅✅✅✅ | ✅✅✅✅✅✅✅`

**Skin Care** (3 weeks only, then archived):  
`✅✅✅✅✅✅✅ | ✅✅❌❌✅✅✅ | ✅✅✅✅✅✅✅ | [ARCHIVED]`

**Play Music** (Rest every 5th day):  
`✅✅✅✅❌✅✅ | ✅✅❌✅✅✅✅ | ❌✅✅✅✅❌✅ | ✅✅✅❌✅✅✅`

### Weekly Habits (4-week period)

**Finance Check** (Perfect, Sundays):  
`✅ (Sun) | ✅ (Sun) | ✅ (Sun) | ✅ (Sun)`

**Water Plants** (Missed week 2, Saturdays):  
`✅ (Sat) | ❌ | ✅ (Sat) | ✅ (Sat)`

---

## Usage in Automated Tests

### Test Assertions

```python
# Test exact habit count
assert len(get_all_habits(include_inactive=False)) == 4  # Active only
assert len(get_all_habits(include_inactive=True)) == 5   # All habits

# Test perfect streaks
assert calculate_longest_streak("Read Journal") == 28
assert calculate_longest_streak("Finance Check") == 4

# Test broken streaks
assert calculate_longest_streak("Skin Care") == 11  # Before archiving
assert calculate_longest_streak("Water Plants") == 2  # After recovery

# Test regular gaps
assert calculate_longest_streak("Play Music") == 4

# Test champion identification
champion_name, streak = get_longest_streak_all_habits()
assert champion_name == "Read Journal"
assert streak == 28

# Test inactive habit exclusion
active_names = [h.name for h in get_all_habits(include_inactive=False)]
assert "Skin Care" not in active_names

# Test inactive habit inclusion
all_names = [h.name for h in get_all_habits(include_inactive=True)]
assert "Skin Care" in all_names

# Test inactive habit data retention
skin_care = find_by_name("Skin Care", include_inactive=True)
assert skin_care.is_active == False
events = find_events_by_habit_id(skin_care.habit_id)
assert len(events) == 19  # Exactly 19 events preserved

# Test completion counts
read_events = get_events("Read Journal")
assert len(read_events) == 28  # Perfect completion

play_events = get_events("Play Music")
assert len(play_events) == 22  # 28 days - 6 rest days

finance_events = get_events("Finance Check")
assert len(finance_events) == 4  # 4 weeks

water_events = get_events("Water Plants")
assert len(water_events) == 3  # 4 weeks - 1 missed
```

---

## Realistic Behavior Patterns

Each habit reflects real-world usage scenarios:

### 1. **Read Journal** (Perfect Discipline)
- Dedicated reader with unwavering commitment
- **Lesson**: Shows achievable 100% consistency
- **Psychology**: Habit fully integrated into routine

### 2. **Skin Care** (Life Changes)
- Consistent for 3 weeks, then routine changed
- **Lesson**: Habits can be abandoned or replaced
- **Psychology**: Demonstrates realistic lifecycle

### 3. **Play Music** (Strategic Rest)
- Structured practice with intentional recovery
- **Lesson**: Rest prevents burnout
- **Psychology**: Sustainable long-term approach

### 4. **Finance Check** (Weekly Ritual)
- Disciplined weekly review every Sunday
- **Lesson**: Weekly habits can be as consistent as daily
- **Psychology**:  Anchored to specific day/time

### 5. **Water Plants** (Occasional Disruption)
- Generally consistent with travel interruption
- **Lesson**: Life events disrupt even good habits
- **Psychology**: Demonstrates recovery and continuation

---

## Data Integrity Guarantees

### ✅ Guaranteed Properties

1. **Exact counts**: All completion counts are deterministic
2. **Reproducible**: Same seed data every time
3. **Complete coverage**: Tests all major features
4. **Realistic patterns**: Mirrors actual user behavior
5. **Edge cases**: Includes breaks, gaps, and perfect runs

### ✅ Validation Checks

- ✅ Total habits:  Exactly 5
- ✅ Active habits:  Exactly 4
- ✅ Inactive habits: Exactly 1 (Skin Care)
- ✅ Read Journal events:  Exactly 28
- ✅ Skin Care events: Exactly 19
- ✅ Play Music events: Exactly 22
- ✅ Finance Check events: Exactly 4
- ✅ Water Plants events:  Exactly 3
- ✅ All habits have non-empty descriptions
- ✅ All events have habit_id foreign keys
- ✅ Inactive habit (Skin Care) has is_active = False

---

## Conclusion

These test fixtures provide **comprehensive, predictable, and realistic** data for testing all aspects of the habit tracker application: 

- ✅ **Specification compliant**:  Exactly 4 weeks (28 days) of data
- ✅ **Complete coverage**: Tests all features (streaks, analytics, status, archive)
- ✅ **Functional programming**: Analytics use map, filter, sorted, comprehensions
- ✅ **Realistic patterns**: Mirrors actual user behavior
- ✅ **Deterministic**: Same results every time
- ✅ **Well-documented**: Clear expected values for all tests

The fixtures enable confident automated testing and serve as executable documentation of the application's behavior.



