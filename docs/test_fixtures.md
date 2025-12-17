# Test Fixture Data Specification

This document describes the predefined tracking data (test fixtures) for the 5 seeded habits over a 4-week period.

## Overview

- **Period**: Exactly 4 weeks (28 days) from the current date backward
- **Purpose**: Consistent, predictable data for testing analytics and streak calculations
- **Habits**: 5 predefined habits with different tracking patterns
- **Status**: 4 active habits + 1 inactive habit (for testing archive functionality)

---

## Habit 1: Read Journal (Daily) ✅ ACTIVE

**Pattern**: Perfect completion streak - most disciplined habit

**Status**: ✅ **ACTIVE**

| Week | Completions | Notes |
|------|-------------|-------|
| Week 1 | 7/7 | All days completed |
| Week 2 | 7/7 | All days completed |
| Week 3 | 7/7 | All days completed |
| Week 4 | 7/7 | All days completed |

**Total**: 28/28 completions  
**Longest Streak**: 28 days  
**Current Streak**: 28 days  
**Success Rate**: 100%

**Notes Pattern**: Alternates between "Morning reading session" and "Evening reading session"

**Use Case**: Test perfect streak calculation, validate daily habit tracking with 100% completion

---

## Habit 2: Skin Care (Daily) ❌ INACTIVE

**Pattern**: Tracked for 3 weeks with good consistency, then archived (routine changed)

**Status**: ❌ **INACTIVE** (Archived)

| Week | Completions | Notes |
|------|-------------|-------|
| Week 1 | 7/7 | Days 1-7 completed |
| Week 2 | 5/7 | Days 10, 11 missed (busy weekend) |
| Week 3 | 7/7 | Days 15-21 completed |
| Week 4 | - | Habit archived (not tracked) |

**Total**: 19/21 completions (tracked for 3 weeks only)  
**Longest Streak**: 11 days (days 12-21 after week 2 break, then 1 day of week 4)  
**Current Streak**: 0 (archived)  
**Success Rate**: 90. 5% (while active)

**Notes Pattern**: "Full routine completed" every 3rd day, otherwise "Morning routine"

**Use Case**: 
- ✅ Test that inactive habits are hidden from active lists
- ✅ Test that inactive habits appear in "List all habits (including inactive)"
- ✅ Test that inactive habits retain their historical data
- ✅ Test that archived habits can be reactivated via edit
- ✅ Test that inactive habits cannot be checked off
- ✅ Test status indicator in UI (strikethrough, dim styling)

---

## Habit 3: Play Music (Daily) ✅ ACTIVE

**Pattern**: Practice schedule with regular rest days (every 5th day off)

**Status**: ✅ **ACTIVE**

| Week | Completions | Notes |
|------|-------------|-------|
| Week 1 | 6/7 | Day 5 skipped (rest day) |
| Week 2 | 5/7 | Days 10, 15 skipped (rest days) |
| Week 3 | 6/7 | Day 20 skipped (rest day) |
| Week 4 | 5/7 | Day 25 skipped (rest day) |

**Total**: 22/28 completions  
**Longest Streak**: 4 days  
**Current Streak**: 3 days  
**Success Rate**:  78.6%

**Notes Pattern**: Rotates through "Piano practice", "Guitar session", "Vocal exercises", "Music theory"

**Use Case**: Test multiple short streaks with regular gaps, realistic practice schedule

---

## Habit 4: Finance Check (Weekly) ✅ ACTIVE

**Pattern**:  Perfect weekly completion (every Sunday) - consistent financial discipline

**Status**: ✅ **ACTIVE**

| Week | Completions | Notes |
|------|-------------|-------|
| Week 1 | ✅ | Sunday completed |
| Week 2 | ✅ | Sunday completed |
| Week 3 | ✅ | Sunday completed |
| Week 4 | ✅ | Sunday completed |

**Total**: 4/4 completions  
**Longest Streak**: 4 weeks  
**Current Streak**: 4 weeks  
**Success Rate**: 100%

**Notes Pattern**: Rotates through different financial tasks (budget review, investments, bills, savings)

**Use Case**: Test weekly habit tracking, validate week normalization logic, perfect weekly streak

---

## Habit 5: Water Plants (Weekly) ✅ ACTIVE

**Pattern**:  Missed week 2 (broken weekly streak - was traveling)

**Status**: ✅ **ACTIVE**

| Week | Completions | Notes |
|------|-------------|-------|
| Week 1 | ✅ | Saturday completed |
| Week 2 | ❌ | Missed (traveling) |
| Week 3 | ✅ | Saturday completed |
| Week 4 | ✅ | Saturday completed |

**Total**: 3/4 completions  
**Longest Streak**: 2 weeks (weeks 3-4)  
**Current Streak**: 2 weeks  
**Success Rate**: 75%

**Notes Pattern**: Detailed plant care notes including watering, pest checks, trimming, fertilizing

**Use Case**: Test weekly streak breaks, validate weekly habit with single missed week, current streak recovery

---

## Summary Statistics

### Active Habits (4)

| Habit | Type | Completions | Longest Streak | Success Rate |
|-------|------|-------------|----------------|--------------|
| Read Journal | Daily | 28/28 | 28 days | 100% |
| Play Music | Daily | 22/28 | 4 days | 78.6% |
| Finance Check | Weekly | 4/4 | 4 weeks | 100% |
| Water Plants | Weekly | 3/4 | 2 weeks | 75% |

### Inactive Habits (1)

| Habit | Type | Completions | Longest Streak | Success Rate |
|-------|------|-------------|----------------|--------------|
| Skin Care | Daily | 19/21 | 11 days | 90.5% |

---

## Testing Scenarios Covered

### Streak Calculations
- ✅ Perfect daily streak (28 days) - Read Journal
- ✅ Multiple short daily streaks - Play Music (4-day max with regular gaps)
- ✅ Perfect weekly streak - Finance Check (4 weeks)
- ✅ Broken weekly streak with recovery - Water Plants (1 week, break, 2 weeks)
- ✅ Archived habit with historical data - Skin Care (11-day longest streak before archiving)

### Analytics
- ✅ Longest streak overall:  Read Journal (28 days) - **CHAMPION**
- ✅ Two daily active habits with different patterns
- ✅ Two weekly active habits with different patterns
- ✅ One inactive daily habit for archive testing

### Success Rates
- ✅ 100% completion:  Read Journal (daily), Finance Check (weekly)
- ✅ 90.5% completion: Skin Care (inactive, 19/21 while active)
- ✅ 78.6% completion: Play Music (22/28)
- ✅ 75% completion: Water Plants (3/4 weeks)

### Status & Archive Testing
- ✅ Active habits appear in default lists
- ✅ Inactive habit (Skin Care) hidden from active lists
- ✅ Inactive habit appears when including inactive
- ✅ Inactive habit retains all historical data (19 completions)
- ✅ Status indicators in UI (Active vs Archived)

### Edge Cases
- ✅ Consecutive missed days (Skin Care - days 10, 11)
- ✅ Regular pattern with gaps (Play Music - every 5th day)
- ✅ Single week missed (Water Plants - week 2)
- ✅ Different weekly days (Finance:  Sunday, Water Plants: Saturday)
- ✅ Partial period tracking (Skin Care - 3 weeks before archiving)

---

## Expected Analytics Results

### When Listing Active Habits Only

```
📋 Currently tracked habits: 

  Icon  │  Habit Name      │  Periodicity  │  Description
────────┼──────────────────┼───────────────┼──────────────────────────────────────
  📅    │  Read Journal    │    Daily      │  Read a journal (20-35 minutes)
  📅    │  Play Music      │    Daily      │  Practice an instrument for 15-30 min
  📆    │  Finance Check   │    Weekly     │  Review spending and budget/accounts
  📆    │  Water Plants    │    Weekly     │  Water plants and check soil moisture

Total: 4 active habits
```

### When Listing All Habits (Including Inactive)

```
📚 All habits (including inactive):

  Icon  │  Habit Name      │  Periodicity  │  Status   │  Description
────────┼──────────────────┼───────────────┼───────────┼──────────────────────
  📅    │  Read Journal    │    Daily      │  Active   │  Read a journal (20-35 min)
  📅    │  Skin Care       │    Daily      │  Archived │  Complete skincare routine
  📅    │  Play Music      │    Daily      │  Active   │  Practice instrument 15-30 min
  📆    │  Finance Check   │    Weekly     │  Active   │  Review budget/accounts
  📆    │  Water Plants    │    Weekly     │  Active   │  Water plants and check soil

Total: 5 habits (4 active, 1 archived)
```

### Champion Analysis

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
Daily Habits (2 active):
- Read Journal: 28 day streak, 28/28 completions (100%)
- Play Music: 4 day streak, 22/28 completions (79%)

Weekly Habits (2 active):
- Finance Check: 4 week streak, 4/4 completions (100%)
- Water Plants: 2 week streak, 3/4 completions (75%)

Archived Daily Habits (1):
- Skin Care: 11 day streak, 19/21 completions (90.5%)
```

---

## Completion Timeline

### Active Daily Habits (28-day period)

**Read Journal**:  ✅✅✅✅✅✅✅ | ✅✅✅✅✅✅✅ | ✅✅✅✅✅✅✅ | ✅✅✅✅✅✅✅

**Play Music**: ✅✅✅✅❌✅✅ | ✅✅❌✅✅✅✅ | ❌✅✅✅✅❌✅ | ✅✅✅❌✅✅✅

### Inactive Daily Habits (21-day period, then archived)

**Skin Care**: ✅✅✅✅✅✅✅ | ✅✅❌❌✅✅✅ | ✅✅✅✅✅✅✅ | [ARCHIVED]

### Active Weekly Habits (4-week period)

**Finance Check**: ✅ (Sun) | ✅ (Sun) | ✅ (Sun) | ✅ (Sun)

**Water Plants**: ✅ (Sat) | ❌ | ✅ (Sat) | ✅ (Sat)

---

## Usage in Tests

These fixtures enable comprehensive testing: 

```python
# Test champion (longest streak overall)
assert get_longest_streak_all_habits() == ("Read Journal", 28)

# Test perfect daily streak
assert calculate_longest_streak("Read Journal") == 28

# Test regular gaps
assert calculate_longest_streak("Play Music") == 4

# Test perfect weekly streak
assert calculate_longest_streak("Finance Check") == 4

# Test broken weekly streak
assert calculate_longest_streak("Water Plants") == 2

# Test inactive habit NOT in active list
active_habits = get_all_habits(include_inactive=False)
assert "Skin Care" not in [h.name for h in active_habits]
assert len(active_habits) == 4

# Test inactive habit IN all habits list
all_habits = get_all_habits(include_inactive=True)
assert "Skin Care" in [h.name for h in all_habits]
assert len(all_habits) == 5

# Test inactive habit retains data
skin_care = find_by_name("Skin Care", include_inactive=True)
assert skin_care.is_active == False
events = find_events_by_habit_id(skin_care.habit_id)
assert len(events) == 19  # Historical data preserved

# Test inactive habit streak (calculated from historical data)
assert calculate_longest_streak("Skin Care") == 11
```

---

## Realistic Patterns

Each habit reflects real-world usage: 

1. **Read Journal** (Active): Dedicated reader with perfect daily consistency
2. **Skin Care** (Inactive): Was consistent for 3 weeks, then routine changed and archived
3. **Play Music** (Active): Structured practice with intentional rest days (prevents burnout)
4. **Finance Check** (Active): Disciplined weekly review every Sunday
5. **Water Plants** (Active): Generally consistent but occasional travel interruption

The **Skin Care** habit being inactive provides: 
- Realistic scenario (habits get abandoned or replaced)
- Complete test coverage for archive functionality
- Verification that historical data is preserved
- Testing of reactivation through edit feature

These patterns make the test data both **realistic** and **comprehensive** for testing all analytics and status management features. 