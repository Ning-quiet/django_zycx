 /**
  * 
  * @authors Your Name (you@example.org)
  * @date    2021-11-10 23:05:58
  * @version $Id$
  */

 var bodyHeight = $("body").height();
 // 获取底部导航的高度
 var navHeight = $(".navbar").height();
 // 获取显示屏的高度
 var iHeight = document.documentElement.clientHeight || document.body.clientHeight;
 // 如果内容的高度大于（窗口的高度 - 导航的高度）,移除属性样式
 if (bodyHeight > (iHeight - navHeight)) {
   $("#footer").removeClass("navbar-fixed-bottom");
 }