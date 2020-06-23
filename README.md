# 建议Iteration设置

| 种类 | Interactive Mode Iteration | Batch Mode Iteration |
| :--: | :------------------------: | :------------------: |
| 帽子 |             3              |          10          |
| 手套 |             6              |     Unavailable      |
| 围巾 |         Not Tested         |     Unavailable      |

# 各模式综述

### Single File Mode

作为软件的最初原型而开发，功能可以被`Interactive Single Mode` 完全替代

### Batch Mode

* 批量处理模式，适合处理形状规则的帽子图片，平均每张帽子图片处理时间为2.5mi
* 不适合处理手套围巾

### Interactive Single Mode

单文件处理模式，适合处理帽子、手套，需要在图片上圈定矩形区域 (Region of Interest, ROI)，以区分背景和前景

平均每张处理时间1～10秒（取决于图片的像素大小）

# 如何启动程序（Windows）

1. 点击Windows桌面左下角的`开始`按钮

2. 搜索`anaconda PowerShell Prompt (miniconda)`

<img src="archive/start.png" alt="start" style="zoom:75%;" />

1. 点击搜索得到的`anaconda PowerShell Prompt (miniconda)`， 进入如下界面

<img src="archive/prompt.png" alt="prompt" style="zoom:75%;" />

1. 输入命令`conda activate cv`，若出现如下界面则命令输入正确，关键是光标所在行的开头为`(cv)`

<img src="archive/activate.png" alt="activate" style="zoom:75%;" />

5. 运行程序
   * 方法一：
     1. 输入命令`python `，注意python后面必须要加空格
     2. 打开桌面上的`GrabCut`文件夹，将`main`拖入`Anaconda PowerShell Prompt`
     3. 键入回车键
   * 方法二：
     1. 输入命令` python C:\Users\A201607\Desktop\GrabCut\main.py`
     2. 键入回车

<img src="archive/main.png" alt="main" style="zoom:75%;" />

6. 若操作无误，应该出现以下界面

<img src="archive/appMain.png" alt="appMain" style="zoom:75%;" />

# 点击按钮`Single File Mode`，会进入如下界面

<img src="archive/Single.png" alt="Single" style="zoom:75%;" />

* 该模式一次只能处理一张图片
* `Open`按钮会打开一个文件选择界面，从中选择一张图片即可在主界面中显示出来
* `Save`按钮会打开一个文件保存界面，选择一个文件夹来保存图片
* `Process`按钮会自动扣图
  * 该过程需要3～4分钟，请耐心等待
  * 不要多次点击`Process`按钮，否则程序会重复处理同一张图片
  * 过程中光标会变成圆环
  * 当光标复原，或`Anaconda PowerShell Prompt`中出现`Process Completed`时，图片处理完成
* `quit`会退出`Single File Mode`

# 点击按钮`Batch Mode`，会进入如下界面

<img src="archive/Batch.png" alt="Batch" style="zoom:75%;" />

* `Choose Directory `会
  * 打开一个文件夹选择界面，选择需要批处理的图片所在的文件夹
  * 选择完文件夹后，会在所选文件夹下创建一个名为`results`的文件夹
  * 若`results`文件夹原本存在，则会**删除原文件夹及其包含的所有文件**，再创建一个新的、空的`results`文件夹
* `Start Processing` 会开始处理所选的图片
* `Iteration` 设置算法的循环次数
  * 输入数值后，键入回车键，以设置循环次数
  * 设置成功后，会在`log`中显示`Current iteration = newIterationTimes `
* `Selected Files` 会显示所选目录下可以处理的图片的名字
* `log` 会显示程序的执行情况，包括
  * 处理完成的图片所在的保存文件夹
  * 图片已经被读入程序
  * 图片已经被处理完成
  * 图片已经被保存
* `Completed Files`，会显示已经保存的图片名字及其总的处理时间

# 点击按钮`Interactive Single Mode`，会进入如下界面



<img src="archive/InteractiveSingleMode.png" alt="InteractiveSingleMode" style="zoom:40%;" />

## 使用流程

1. 点击`open` 按钮，会弹出文件选择界面，选择一个图片文件 (支持：jpg, png)

<img src="archive/openISM.png" alt="InteractiveSingleMode" style="zoom:40%;" />

1. 使用`Compress`下拉框改变图片的压缩方式，压缩后的图片像素会显示在`Compressed W H`
2. `W`  代表横向像素数量 `H` 代表纵向像素数量
   1. `Original W H` 显示图片原本的像素
   2. `Compressed W H` 显示图片在所选压缩方式下的像素
   3. `Saved W H` 代表图片经自动抠图处理后、剪裁为ROI (见第5条) 所选区域后的像素
3. `Iteration` 设置算法的循环次数
   * 输入数值后，键入回车键，以设置循环次数
   * 设置成功后，会在`log`中显示`Current iteration = newIterationTimes `

5. 点击`Process` 按钮后，会出现一个名为`Select ROI` 的窗口

<img src="archive/ROI.png" alt="InteractiveSingleMode" style="zoom:40%;" />

* 按住鼠标左键并拖动，窗口中会出现蓝色矩形框 (即为ROI)，调整至蓝色矩形框完全包含待截取物体，并有充分的框外空间作为背景
* 按空格或回车键确定ROI
* 按c取消选择

6. 用空格或回车键确定ROI后，出现如下界面，处理后的图片自动显示在app界面中

   <img src="archive/processed.png" alt="InteractiveSingleMode" style="zoom:40%;" />

7. 点击`Save`按钮，会将自动抠图后、剪裁为ROI的图片存到原图所在文件夹中新建的`result`文件夹中，`Saved W H` 更新为保存的图片的像素，图为保存的图片

<img src="archive/hat_2.jpg" alt="InteractiveSingleMode" style="zoom:40%;" />