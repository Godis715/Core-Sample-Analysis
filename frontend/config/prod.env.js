'use strict'
module.exports = {
  NODE_ENV: '"production"',
  API_URL: JSON.stringify(process.env.VUE_APP_API_URL),
  API_PORT: JSON.stringify(process.env.VUE_APP_API_PORT)
}