// pages/title/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    token: '',
    imgSrc: '',
    isShowDetail: false,
    resultList: [],
    baseData: '',
    wordLine: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    let that = this;
    let grant_type = 'client_credentials';
    let client_id = 'KWK2y9G1OpMHeEme2DvPk87b';
    let client_secret = 'TlyeV35u9DMd0xicyMQ3M2SR5qmd6NGF';
    wx.request({
      url: 'https://aip.baidubce.com/oauth/2.0/token?grant_type=' + grant_type + '&client_id=' + client_id + '&client_secret=' + client_secret,
      method: 'post',
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        that.setData({
          token: res.data.access_token
        });
      }
    })
  },
  loadImage() {
    let that = this;
    wx.chooseImage({
      count: 0,
      sizeType: ['original', 'compressed'], //原图 / 压缩
      sourceType: ['album', 'camera'], //相册 / 相机拍照模式
      success(res) {
        that.setData({
          imgSrc: res.tempFilePaths[0]
        });
        //将图片转换为Base64格式
        wx.getFileSystemManager().readFile({
          filePath: res.tempFilePaths[0],
          encoding: 'base64',
          success(data) {
            let baseData = data.data; //'data:image/png;base64,' + data.data;
            that.setData({
              baseData: baseData
            });
          }
        });
      }
    })
  },
  //图像识别
  identify() {
    let that = this;
    let requestData = {
      'image': that.data.baseData
    };
    wx.request({
      url: 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + that.data.token,
      method: 'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      data: requestData,
      success: function (identify) {
        console.log(identify.data.words_result);
        that.setData({
          isShowDetail: true,
          wordLine: identify.data.words_result_num,
          resultList: identify.data.words_result
        });
      }
    })
  },
    //上传数据
    data: {
      resultText: '' // 用于绑定文本框的数据
    },
  
    shangchuan: function (e) {
      var that = this; // 保存当前页面实例的引用
  
      wx.request({
        url: 'http://localhost:8080/demo2',
        method: 'POST',
        data: {
          data: e.currentTarget.dataset.id
        },
        success(res) {
          console.log("上传数据成功", res);
        
          // 在这里处理服务器返回的数据
          if (res.data.success) {
            // 从服务器返回的结果中获取 result 字段
            var resultFromServer = res.data.result;
        
            // 将结果设置到 data 中的 resultText 属性
            that.setData({
              resultText: resultFromServer
              
            }, function() {
              // 在setData回调中执行你需要的操作
              // 在小程序界面上提示上传数据成功
              wx.showToast({
                title: '上传数据成功',
                icon: 'success',
                duration: 2000
              });
            });
          } else {
            console.log("上传数据失败", res);
            // 在小程序界面上提示上传数据失败
            wx.showToast({
              title: '上传数据失败',
              icon: 'none',
              duration: 2000
            });
          }
        
          // ...
        },
        fail(res) {
          console.log("上传数据失败", res);
          // 在小程序界面上提示上传数据失败
          wx.showToast({
            title: '上传数据失败',
            icon: 'none',
            duration: 2000
          });
        }
        
      });
    }

})
