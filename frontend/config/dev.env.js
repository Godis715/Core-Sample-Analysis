'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: JSON.stringify(process.env.VUE_APP_API_URL),
  API_PORT: JSON.stringify(process.env.VUE_APP_API_PORT)
})
