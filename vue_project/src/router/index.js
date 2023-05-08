import Vue from 'vue'

import Home from '../views/HomePage.vue'
import Login from '../views/LoginPage.vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [{
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    //路由嵌套
    children: [
      { path: '/home/menu1',name:'Menu1', component: () => import('../components/Main1.vue') },
      { path: '/home/menu2',name:'Menu2', component: () => import('../components/Main2.vue') },
      { path: '/home/menu3',name:'Menu3', component: () => import('../components/Main3.vue') }
    ]
  }
  ]
})


//路由守卫，在执行路由前执行本方法来做认证操作
// to:要去的路径,from:获取从那个页面路径跳转而来的,next:放行
// router.beforeEach((to, from, next) => {
//   // 判断当前路径是否为login ，如果是true 着放行
//   if (to.path === '/login') return next();
//   //获取当前token
//   const token = window.sessionStorage.getItem('token');
//   //如果当前token为空，着返回到login页面
//   if (!token) return next('/login');
//   //如果上面全部都过了，那么执行放行
//   next();
// })

export default router
