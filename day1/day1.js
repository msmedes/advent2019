const fs = require('fs')

const read_file = filename => {
  try {
    var data = fs.readFileSync(filename, 'utf8')
    return data.split('\n')
  } catch (e) {
    console.log('Error:', e.stack)
  }
}

const fuel = mass => {
  return Math.floor(mass / 3) - 2
}

const sum_fuel = masses => {
  return masses.reduce((a, b) => a + fuel(b), 0)
}

console.log(sum_fuel(read_file('input.txt')))
