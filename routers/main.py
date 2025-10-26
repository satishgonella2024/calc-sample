# API Routes

const express = require('express');
const router = express.Router();

// Calculator state
let currentValue = 0;
let operator = null;
let prevValue = null;

// GET /api/calculator - Get the current state of the calculator
router.get('/api/calculator', (req, res) => {
  res.json({ currentValue, operator, prevValue });
});

// POST /api/calculator/calculate - Perform a calculation
router.post('/api/calculator/calculate', (req, res) => {
  const { value, op } = req.body;

  switch (op) {
    case '+':
      currentValue = prevValue + value;
      break;
    case '-':
      currentValue = prevValue - value;
      break;
    case '*':
      currentValue = prevValue * value;
      break;
    case '/':
      currentValue = prevValue / value;
      break;
    default:
      return res.status(400).json({ error: 'Invalid operation' });
  }

  prevValue = currentValue;
  operator = null;
  res.json({ currentValue });
});

module.exports = router;