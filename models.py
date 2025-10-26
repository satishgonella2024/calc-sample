# Models

## Calculation

@description('A simple calculation')
model Calculation {
  @prompt('First operand')
  operand1 Float

  @prompt('Second operand')
  operand2 Float

  @prompt('Operator')
  operator String

  @computed
  result Float
}