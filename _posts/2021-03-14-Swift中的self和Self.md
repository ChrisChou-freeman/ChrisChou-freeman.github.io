---
layout:     post
title:      Swift中的self和Self
subtitle:   Swift基础（二）
date:       2021-03-14
author:     ChrisChou
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - Swift
---

> Swift 这个语言的特性是我接触过的语言中最多的，语法糖也是多的不行，对于一个想要知道所有原理的人去学这个语言是相当的难受，感觉会被逼疯。对于那些注重业务层只想实现效果的人会觉得非常的爽


## Swift中的self（小写开头）和Self（大写开头）的区别

### **关于self(小写开头)**
苹果官方的swift教程中很多地方，关于类或者结构调用自身实例的方法都会，忽略掉self而直接调用局部变量或者常量一样调用，这一点让我有点抓狂，每次在类或者结构中这样使用对象的参数的时候，我都会犹豫一下，这是局部变量，包里的变量，还是全局变量。过于反直觉了，还是python比较合理一点，必须要通过self本身来返回对象本身的变量。非常符合第一直觉。

如下代码
```swift
import SwiftUI

struct LandmarkRow: View {
    var landmark: Landmark
    
    var body: some View {
        HStack {
            landmark.image
                .resizable()
                .frame(width: 50, height: 50)
            Text(landmark.name)
            Spacer()
            if landmark.isFavorite{
                Image(systemName: "star.fill")
                    .foregroundColor(.yellow)
            }
        }
    }
}
```
再计算属性body中的landmark是可以直接调用的，这一点和C#一样，但是我还是喜欢加上self，这样更明白一点
```swift
import SwiftUI

struct LandmarkRow: View {
    var landmark: Landmark
    
    var body: some View {
        HStack {
            self.landmark.image
                .resizable()
                .frame(width: 50, height: 50)
            Text(self.landmark.name)
            Spacer()
            if self.landmark.isFavorite{
                Image(systemName: "star.fill")
                    .foregroundColor(.yellow)
            }
        }
    }
}
```
self 其实说白了就是实例本身

### **关于Self（大写开头）**
初次看到这个大写开头的Self的时候，心里是WTF的状态，莫名其妙的它的作用和self（小写开头）还是有区别的，self通常是代表实例本身，可以用来调用实例的变量和常量，或者实例方法。 但是Self(大写开头)就不一样了，它通常有连个作用

#### **作用1**

用于调用 类/结构 的Static修饰的 类/结构 参数， 或者方法。

例如
```swift
struct BadgeSymbol: View {
    static let symbolColor = Color(red: 79.0 / 255, green: 79.0 / 255, blue: 191.0 / 255)
    var body: some View {
        GeometryReader { geometry in
             Path { path in
                 let width = min(geometry.size.width, geometry.size.height)
                 let height = width * 0.75
                 let spacing = width * 0.030
                 let middle = width * 0.5
                 let topWidth = width * 0.226
                 let topHeight = height * 0.488

                 path.addLines([
                     CGPoint(x: middle, y: spacing),
                     CGPoint(x: middle - topWidth, y: topHeight - spacing),
                     CGPoint(x: middle, y: topHeight / 2 + spacing),
                     CGPoint(x: middle + topWidth, y: topHeight - spacing),
                     CGPoint(x: middle, y: spacing)
                 ])
                 
                 path.move(to: CGPoint(x: middle, y: topHeight / 2 + spacing * 3))
                 path.addLines([
                     CGPoint(x: middle - topWidth, y: topHeight + spacing),
                     CGPoint(x: spacing, y: height - spacing),
                     CGPoint(x: width - spacing, y: height - spacing),
                     CGPoint(x: middle + topWidth, y: topHeight + spacing),
                     CGPoint(x: middle, y: topHeight / 2 + spacing * 3)
                 ])
             }
             .fill(Self.symbolColor)
         }
    }
}
```
里面的symbolColor就是属于静态常量，也就是说是属于结构BadgeSymbol的，并不属于实例本身，所以这里用self(小写开头)去调用symbolColor的时候就会报错。

#### **作用2**
Self(大写开头)还有一个作用就是用于拓展里面，在拓展中的时候Self指的就是类型本身，比如Int或者String，直接看代码吧
```swift
extension BinaryInteger {
    func squared() -> Self {
        return self * self
    }
}
```
以上的例子中Self其实等于就是Int本身了，和一下的方法是等同的
```swift
func squared() -> Int {
    return self * self
}
```
而self（小写）本身在这里指的是值本身。

Over