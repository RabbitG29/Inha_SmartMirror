<template>
  <div id="app">
    <div id="nav">
    </div>
    <router-view/>
  </div>
</template>

<style>
@font-face{font-family: 'netmarbleM'; src:url('./fonts/netmarbleM.ttf')}
#app {
  font-family: 'netmarbleM';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #ffffff;
  background-color: black;
}
body{
  margin :0;

}
#nav {
  padding: 30px;
  margin :0px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
