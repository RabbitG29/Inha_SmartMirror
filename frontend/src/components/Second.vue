<template>
  <div class="hello">
    <div class="">
      <h1>{{data4[0]}}년 {{data4[1]}}월 {{data4[2]}}일
      <br>
      <a v-if="data4[3]<10">0</a>{{data4[3]}}:<a v-if="data4[4]<10">0</a>{{data4[4]}}:<a v-if="data4[5]<10">0</a>{{data4[5]}}</h1>
    </div>
    <h2>사진</h2>
     <img v-if="feels[1]>10 || feels[5]>10" id="photo" src="../assets/ang.png" width="200" height="200">
     <img v-else id="photo" src="../../../img/download1.jpg" width="200" height="200">

  </div>
</template>

<script>
export default {
  name: 'Second',
  props: {
    msg: String
  },
  sockets: {
    connect: function(){
      console.log('socket connected')
    },
    date: function(d){
      console.log('get inside date')
      console.log(d)
      this.data4 = d.data
      if(this.data4[5]==0) {
        this.$router.push({
          name: 'HelloWorld'
        })
      }
    },
    receive: function(e){
      console.log('get inside receive')
      console.log(e)
      this.feels = e.data
      console.log(this.feels)
    }
  },
  data () {
    return {
      data4: null,
      feels:[]
    }
  },
  mounted: function() {
    console.log('in mounted')
    this.feels = [0,0,0,0,0,0,0,0]
    this.getInfo()
  },
  methods: {
    getInfo: function(){
      this.$socket.emit('date')
      console.log('getDate called')
    },
    getfeels: function(){
      this.$socket.emit('receive')
      console.log('getReceive called')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@font-face{font-family: 'netmarbleM'; src:url('../fonts/netmarbleM.ttf')}
.hello{
  font-family: 'netmarbleM';
  font-weight: 300;
  padding-bottom: 43px;
}

#photo{
  left :0;
  padding-left: 10px;

}
h1 {
  font-weight: 500;
}
h2{
  font-weight: 500;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
</style>
