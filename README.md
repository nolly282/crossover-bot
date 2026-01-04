# Moving Average Crossover Trading Bot (MetaTrader 5)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![MT5](https://img.shields.io/badge/Platform-MetaTrader%205-green)

## Important Disclaimer

**This bot is for educational and experimental purposes only.**

It is fully capable of connecting to live market data and executing real trades via MetaTrader 5.  
**However, it was not designed or tested for live trading with real capital.**  
Always run it on a **demo account** first. Use at your own risk — no guarantees are provided.

---

## Project Overview

This repository contains a Python-based algorithmic trading bot that implements a classic **Moving Average (MA) Crossover** strategy on the **MetaTrader 5** platform.

The bot runs continuously, monitors price action in real-time, detects MA crossovers, and automatically executes and manages trades according to predefined rules.

---

## Strategy Logic

### Entry Conditions

**Long (Buy):**
- Fast MA crosses **above** the Slow MA
- Current candle closes **above** the Slow MA (for confirmation)

**Short (Sell):**
- Fast MA crosses **below** the Slow MA
- Current candle closes **below** the Slow MA (for confirmation)

### Exit Conditions

An open position is closed when **any** of the following occurs:
- An opposite MA crossover is detected (trend reversal signal)
- Take-profit level is reached (configurable)

---

## Core Features

- Real-time data streaming via the MetaTrader 5 Python API
- Rolling Simple Moving Average calculations using `pandas`
- Robust crossover detection with close-price confirmation
- Automated market order execution (buy/sell)
- Position monitoring to prevent duplicate trades
- Trade-flag system to avoid multiple orders on the same candle
- Continuous polling loop with sleep control for efficiency
- Basic risk safeguards (no overlapping positions)

---

## Project Context

This bot was my **first fully functional algorithmic trading system** and served as a foundational project for learning:

- Reliable integration with the MT5 API
- Real-time state management in live trading environments
- Safe and predictable trade execution logic
- Preventing common pitfalls (duplicate orders, missed signals)

It focuses on **correctness and robustness** over complex optimization.

---

## Setup & Running Instructions

See [`installation.md`](installation.md) for detailed steps on:
- Required software (MetaTrader 5 + Python integration)
- Dependencies installation
- Configuration
- How to launch the bot

---

## Author

**Chukwunomso Anadumaka**  
📧 Email: chinonsoanadumaka@gmail.com  

Feel free to reach out for questions, suggestions, or collaboration opportunities.

---

*Happy coding and safe trading!*