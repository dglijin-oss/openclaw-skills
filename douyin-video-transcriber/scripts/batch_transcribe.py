#!/usr/bin/env python3
"""批量下载抖音视频 + Whisper 转写 - 完整版"""
import os, sys, json, time, tempfile, subprocess, whisper, requests
from datetime import datetime
from pathlib import Path

WHISPER_MODEL = "base"
DEFAULT_OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "video-transcriber"

# 所有视频URL已通过浏览器获取
VIDEOS = [
    {"id": "7594031728987498459", "desc": "化橘红的禁忌与作用", "likes": 464, "url": "https://v26-web.douyinvod.com/d33590ada666cf979f1641990a5b8bb5/69e61228/video/tos/cn/tos-cn-ve-15/ogfIoDaB2pbkIgE6afqFQAlDBOJaYE9kpnCAQA/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=574&bt=574&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrK5rM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=O2Q7aTllZDdoOWVoZjY3M0BpMzZ4Nm05cmxwODMzNGkzM0BeXzIxYDU1NWExYjYwMl5gYSNhaGNoMmQ0aGVhLS1kLS9zcw%3D%3D&btag=c0000e00028000&cquery=100B_100x_100z_100o_100w&dy_q=1776674671&feature_id=0ea98fd3bdc3c6c14a3d0804cc272721&l=202604201644311F24604CC698C507DDE2&__vid=7594031728987498459"},
    {"id": "7594147461460516977", "desc": "化橘红怎么挑选？最硬核干货", "likes": 329, "url": "https://v26-web.douyinvod.com/2a120583cd2fbaa154176ebb52dec839/69e60b75/video/tos/cn/tos-cn-ve-15c000-ce/okI9x9BpSYkYOFiEfLhDuwQAnOEfAKVKWEGnE9/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=407&bt=407&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKhCM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=Nmc4ZjU1ZWVkOWllNzY6N0Bpamh0c3k5cjV3ODMzbGkzNUA1M14vYTVgNWMxMC4uLjRhYSMyMW5eMmRrNGVhLS1kLTRzcw%3D%3D&btag=80000e00028000&cquery=100z_100o_100w_100B_100x&dy_q=1776672970&feature_id=0ea98fd3bdc3c6c14a3d0804cc272721&l=202604201616109CD4AB0F977E1AABCD44&__vid=7594147461460516977"},
    {"id": "7621859829086493951", "desc": "怎么才能买到正宗的化橘红", "likes": 62, "url": "https://v26-web.douyinvod.com/92285b0c689e2817854511a6bdac68bf/69e60b3c/video/tos/cn/tos-cn-ve-15/o0wiQyDBRyAIcB2OiQUb1aGvLJEIQdPvFAZFc/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=694&bt=694&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKECM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=NzhoaGQ6Zjg7OWU5Njs0NkBpam80ZnA5cjQ3OjMzNGkzM0BeM2M1YGNiXzMxYy8xLzEwYSMubWY0MmRrZjBhLS1kLTBzcw%3D%3D&btag=80000e00028000&cquery=100w_100B_100x_100z_100o&dy_q=1776672974&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=2026042016161498B2C58D2C7DC3D25F95&__vid=7621859829086493951"},
    {"id": "7617558497748287401", "desc": "化橘红是什么", "likes": 58, "url": "https://v26-web.douyinvod.com/37ae513c8d3d0363d9f07918a7419f13/69e60b43/video/tos/cn/tos-cn-ve-15/o0wAatg9ZFkcABDFSp9j9zgKCEQEfACDIu4SeW/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=640&bt=640&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrK2CM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=OWUzMzxpNGU1PDo5aDg7aEBpMzQ4ZXg5cjtqOTMzNGkzM0A0LjY2Li1iXzExYS8xM2NfYSM0MTZqMmRzLm9hLS1kLTBzcw%3D%3D&btag=80000e00028000&cquery=100x_100z_100o_100w_100B&dy_q=1776672979&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=20260420161619B16ADE517AC59356BD68&__vid=7617558497748287401"},
    {"id": "7605934593636253092", "desc": "什么是天理？什么又是公平", "likes": 53, "url": "https://v26-web.douyinvod.com/ce02293ac9ec0c77708907d94f4c1756/69e60b2b/video/tos/cn/tos-cn-ve-15/o4pBgKLGZIGDx4QAlf1AeOIfTNEt755BGC62uC/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=638&bt=638&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrK-CM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=ZDtpaGQ6Njw2M2Y2NmRoZUBpamZtc3g5cmh1OTMzNGkzM0A2Mi8zMy4tNTUxLjE2XjEzYSNzLW80MmQ0NjNhLS1kLTBzcw%3D%3D&btag=80000e00018000&cquery=100o_100w_100B_100x_100z&dy_q=1776672983&feature_id=0ea98fd3bdc3c6c14a3d0804cc272721&l=20260420161623B16ADE517AC59356BEF2&__vid=7605934593636253092"},
    {"id": "7608882483228238761", "desc": "化橘红是什么？药食同源", "likes": 52, "url": "https://v26-web.douyinvod.com/efaefd9b633d2c83dc253742bf0f0c2c/69e60b5d/video/tos/cn/tos-cn-ve-15/oMQsR9Bp7mY23FRolAKDxggADYAfACOeBIK3EC/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=540&bt=540&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKzCM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=PDk6OTVlNDs1MzU3MzhoZUBpM2Y1cGw5cmo1OTMzNGkzM0BhMC9gXjYyNWMxNWBeLTEzYSMtZXBnMmRrY2BhLS1kLTBzcw%3D%3D&btag=80000e00028000&cquery=100w_100B_100x_100z_100o&dy_q=1776672987&feature_id=0ea98fd3bdc3c6c14a3d0804cc272721&l=20260420161627949B569E6A6E293E6A72&__vid=7608882483228238761"},
    {"id": "7615855969532636806", "desc": "新手小白入坑化橘红怎么避坑", "likes": 46, "url": "https://v26-web.douyinvod.com/6a9d866986b2f671614314cb2aab8495/69e60b1e/video/tos/cn/tos-cn-ve-15/oAiCiIGSLBg5wCxET2veAEnDhR9IEMQeAmefFI/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=699&bt=699&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKtCM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=OWc8NTw3OTM3OzlmO2Y2ZEBpM2p1Om45cnFpOTMzNGkzM0AwYzAwYC0xXjIxYC5fXzQtYSNjNHNgMmQ0NWxhLS1kLTBzcw%3D%3D&btag=80000e00010000&cquery=100x_100z_100o_100w_100B&dy_q=1776672991&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=202604201616317ACF5289EDD755A591D7&__vid=7615855969532636806"},
    {"id": "7613825274962934675", "desc": "到底什么是良心", "likes": 43, "url": "https://v26-web.douyinvod.com/94db1cd96974e612aae4495a0417487d/69e60b78/video/tos/cn/tos-cn-ve-15/oAMIpEh2VQieDe6CImuAkfGTLzegAEAU9IkUSs/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=817&bt=817&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKSCM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=M2lkNmQ1NGQ4OTc8ODMzZEBpM2R2ZW45cnh1OTMzNGkzM0A0MDJgMjIyX18xLTQuYTMvYSNlNWlwMmRja2hhLS1kLTBzcw%3D%3D&btag=80000e00028000&cquery=100z_100o_100w_100B_100x&dy_q=1776672995&feature_id=0ea98fd3bdc3c6c14a3d0804cc272721&l=2026042016163569BCFC0DA61989942D9E&__vid=7613825274962934675"},
    {"id": "7621410245591942582", "desc": "正宗化橘红避坑！真假决赛圈", "likes": 42, "url": "https://v26-web.douyinvod.com/caa4e8cd636996dcad4b188c9404d3d7/69e60bdc/video/tos/cn/tos-cn-ve-15/okGPEIAc6jpwxvKi7LjaOQAUQpMHBSi3vPIGG/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=643&bt=643&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKPCM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=PGQ7Ozc1aGY0aDQ5ZzpoNUBpM2Q5eHE5cnRkOjMzNGkzM0BhNTA1NDJgXmIxYjZiMjYuYSM0M3FsMmRrcy9hLS1kLTBzcw%3D%3D&btag=80000e00028000&cquery=100o_100w_100B_100x_100z&dy_q=1776672999&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=2026042016163998B2C58D2C7DC3D26954&__vid=7621410245591942582"},
    {"id": "7617734479788286867", "desc": "正宗化橘红到底有多牛", "likes": 37, "url": "https://v26-web.douyinvod.com/7d586298cfddc17fdf75a1b96f627f30/69e60b4e/video/tos/cn/tos-cn-ve-15/oo6pBvqIEoZFsVvAxgeQt0lC9CH2DAgtAfUInD/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=639&bt=639&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKTCM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=Nzs8aTw5aDk1aGk2aDc0aEBpM21nO3A5cmR0OTMzNGkzM0AvNl8uXjNiXzAxLTFhLl4wYSNxYHNtMmQ0Lm9hLS1kLTBzcw%3D%3D&btag=80000e00020000&cquery=100w_100B_100x_100z_100o&dy_q=1776673003&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=20260420161643B16ADE517AC59356C586&__vid=7617734479788286867"},
    {"id": "7605308409885341686", "desc": "化橘红最容易踩的两种坑", "likes": 37, "url": "https://v26-web.douyinvod.com/2ea14fc242ffaffce923e99835212932/69e60ba7/video/tos/cn/tos-cn-ve-15/oMn9AexuGBUTLfqBzuIrvegwFCGREsGAb07GJA/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=649&bt=649&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKeCM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=NGZmPDtnNWdpNDs5Z2g8M0BpamZkbHA5cmhxOTMzNGkzM0BfYTQ2NGFeNTUxNS4uNmFfYSNhMHFsMmRjZjJhLS1kLTBzcw%3D%3D&btag=c0000e00028000&cquery=100o_100w_100B_100x_100z&dy_q=1776673017&feature_id=0ea98fd3bdc3c6c14a3d0804cc272721&l=20260420161657CE620AC55B01B8BC4891&__vid=7605308409885341686"},
    {"id": "7625709596817317062", "desc": "化橘红搭配方法", "likes": 32, "url": "https://v26-web.douyinvod.com/6d73b266d665abd19e0f1a3919c2139d/69e60b80/video/tos/cn/tos-cn-ve-15/oQRGnTAZesBeDE8AXUsCzQnAIeMLpMaggAeL2u/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=656&bt=656&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKcCM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=ZWY0M2U2OzlpZzdmNzU7OUBpajZmNXA5cjN5OjMzNGkzM0AxMDQvYjY0NTUxYTU1LTZgYSM0NS41MmQ0XzZhLS1kLTBzcw%3D%3D&btag=80000e00028000&cquery=100x_100z_100o_100w_100B&dy_q=1776673021&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=202604201617011DD6C4DA6042F6A293DB&__vid=7625709596817317062"},
    {"id": "7622369809142352233", "desc": "化橘红能不能长期喝", "likes": 32, "url": "https://v26-web.douyinvod.com/c592fa66f90cdb429bd16358148f569b/69e61222/video/tos/cn/tos-cn-ve-15/o4CLAeVk0X8XTBDAgTQMfy8ERCqeAEnSBGkHT7/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=569&bt=569&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKZBM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=N2VnZ2Y8aTpmNjVpZGk3O0Bpam86Z3k5cjM0OjMzNGkzM0BiNi80YzUuNmIxMmJjYDBhYSM1NjJuMmRzZTFhLS1kLTBzcw%3D%3D&btag=80000e00028000&cquery=100w_100B_100x_100z_100o&dy_q=1776674720&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=202604201645209CF116918F680C33CD29&__vid=7622369809142352233"},
    {"id": "7618648187339137961", "desc": "真假化橘红谣言，切勿轻信", "likes": 31, "url": "https://v26-web.douyinvod.com/4e5a6077f9c90c9a8183fe12b383c95c/69e60bbe/video/tos/cn/tos-cn-ve-15/2bf947366b354654864ce70cd231a886/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=676&bt=676&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKk6M4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=PGk4Njc4N2RpNTY0Z2Q6OUBpandwbHc5cm5nOTMzNGkzM0BgMDFgNTQ1Xi0xMjIyMDIvYSNlbmpkMmRjcnFhLS1kLTBzcw%3D%3D&btag=80000e00028000&cquery=100x_100z_100o_100w_100B&dy_q=1776673052&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=20260420161732140C484B1E95ADA8114E&__vid=7618648187339137961"},
    {"id": "7620359251625805523", "desc": "化橘红到底算不算贵", "likes": 27, "url": "https://v26-web.douyinvod.com/55d44d6dff12fb8bfbe8924c5e7c86e2/69e61254/video/tos/cn/tos-cn-ve-15/o83JEAAFLIIeb9QgmdAw98EOEqARDf5BDXApiC/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=883&bt=883&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKlGM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=NWY4ZDU0ODxpPDM8OWVlNkBpM3d2O3g5cjdoOjMzNGkzM0BfYi81LV9eXzAxYDJiMDIvYSNpa2pnMmRjci1hLS1kLTBzcw%3D%3D&btag=c0000e00028000&cquery=100o_100w_100B_100x_100z&dy_q=1776674768&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=202604201646085FA63ADCF98900ABF61F&__vid=7620359251625805523"},
    {"id": "7626297585913855737", "desc": "想买正宗化橘红，却只能听天由命", "likes": 19, "url": "https://v26-web.douyinvod.com/36c32e203adb55e0bc143ed2c0169d45/69e61280/video/tos/cn/tos-cn-ve-15c000-ce/oYEAE1Ao7EAgeGS0oQMxXfQkkwEn8BDnpIK92F/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=627&bt=627&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKmGM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=NWZnNzM6OTg7Zmc1Njo7ZEBpM3hvOW05cmozOjMzbGkzNUAzXmItMDFhNTExNGNiYmFeYSNmNWRzMmQ0bF9hLS1kLTVzcw%3D%3D&btag=80000e00028000&cquery=100x_100z_100o_100w_100B&dy_q=1776674807&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=202604201646462994E5C72E5A884199FB&__vid=7626297585913855737"},
    {"id": "7627451865517462441", "desc": "化橘红避坑方案", "likes": 18, "url": "https://v26-web.douyinvod.com/223b186142b3a2502a735f563427b3af/69e61298/video/tos/cn/tos-cn-ve-15/oEDB7LdAzRWBC25WQSkeN8fLAIAibii0gIsEjC/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=2158&bt=2158&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrK3mM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=OGZoZDdkNTg0Zjo0ZWU2NUBpMzt0OnM5cng1OjMzNGkzM0AzMC0uXjZeXi0xMmAvXjRjYSNqM15vMmRjX2FhLS1kLTBzcw%3D%3D&btag=80000e00028000&cquery=100z_100o_100w_100B_100x&dy_q=1776674850&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=20260420164730479F4BBC5B66A63EEE9C&__vid=7627451865517462441"},
    {"id": "7623859315619143542", "desc": "人心！不可尽信", "likes": 17, "url": "https://v26-web.douyinvod.com/7afd2ddec79f1662a6a1c23b75f5e5dc/69e612cc/video/tos/cn/tos-cn-ve-15/ok35MgMgTfB5E03PChLIAZGNBmA7FbcIQeeNGs/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=646&bt=646&cs=0&ds=6&ft=pEaFx4hZffPdXi~kY13NvAq-antLjrKEvM4nRka70yP_ejVhWL6&mime_type=video_mp4&qs=12&rc=aTo6OWZnM2Y8NDc7Z2ZmOUBpM3RocHI5cjxwOjMzNGkzM0BjMGJiLzEyNV8xLWMwNGJiYSM1YXNjMmRrMzNhLS1kLTBzcw%3D%3D&btag=80000e00028000&cquery=100z_100o_100w_100B_100x&dy_q=1776674894&feature_id=37f92ebd2877ae8e7eba995d406c5150&l=2026042016481460844F8939DDA679F09E&__vid=7623859315619143542"},
]

def download_video(url, path):
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.douyin.com/"}
    with requests.get(url, headers=headers, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    size = os.path.getsize(path)
    if size < 1000:
        raise ValueError(f"文件太小({size}B)")
    return path

def extract_audio(video_path, audio_path):
    cmd = ['ffmpeg', '-i', str(video_path), '-vn', '-acodec', 'libmp3lame', '-y', str(audio_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return False, result.stderr[:300]
    return os.path.exists(audio_path) and os.path.getsize(audio_path) > 0, ""

def transcribe_audio(audio_path):
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(audio=str(audio_path), language='zh', initial_prompt="以下是普通话的句子。")
    return result['text'].strip()

def main():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = DEFAULT_OUTPUT_DIR / f"{timestamp}_profile_report.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"📋 博主: 化州本地奥德彪")
    print(f"📊 共 {len(VIDEOS)} 条视频待处理")
    print(f"📁 输出: {output_file}")
    print()

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 抖音博主视频批量转写报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"博主: 化州本地奥德彪\n")
        f.write(f"主页: https://www.douyin.com/user/MS4wLjABAAAAQi6_ksedvaZshcTY1UQi20yaksLa07peI0MH30hlUbs\n")
        f.write(f"筛选: 点赞最高的前 20 条视频\n\n")
        f.write(f"---\n\n")

    success = 0
    failed = 0
    
    for i, video in enumerate(VIDEOS):
        print(f"\n{'='*50}")
        print(f"[{i+1}/{len(VIDEOS)}] 👍{video['likes']} {video['desc']}")
        print(f"  ID: {video['id']}")
        
        if not video.get("url"):
            print(f"  ⏭️  跳过（无下载URL）")
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"## ⏭️ 视频 {i+1}: {video['desc']}（待补充）\n\n")
                f.write(f"- 视频ID: {video['id']}\n- 点赞: {video['likes']}\n")
                f.write(f"- 状态: 无法获取下载链接\n\n---\n\n")
            failed += 1
            continue
        
        try:
            video_path = Path(tempfile.gettempdir()) / f"dy_{video['id']}.mp4"
            audio_path = Path(tempfile.gettempdir()) / f"dy_{video['id']}.mp3"
            
            print(f"  [1/3] 下载视频...")
            download_video(video['url'], video_path)
            size_mb = os.path.getsize(video_path) / 1024 / 1024
            print(f"  ✓ {size_mb:.1f}MB")
            
            print(f"  [2/3] 提取音频...")
            ok, err = extract_audio(video_path, audio_path)
            if not ok:
                raise Exception(f"音频提取失败: {err}")
            
            print(f"  [3/3] Whisper 转写...")
            transcription = transcribe_audio(audio_path)
            
            for p in [video_path, audio_path]:
                if p.exists():
                    p.unlink()
            
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"## {i+1}. {video['desc']}\n\n")
                f.write(f"- 视频ID: {video['id']}\n")
                f.write(f"- 点赞: {video['likes']:,}\n")
                f.write(f"- 链接: https://www.douyin.com/video/{video['id']}\n\n")
                f.write(f"### 📝 文案\n\n{transcription}\n\n---\n\n")
            
            print(f"  ✅ 完成 ({len(transcription)} 字)")
            success += 1
            
        except Exception as e:
            print(f"  ❌ 失败: {e}")
            # 清理临时文件
            for p in [video_path, audio_path]:
                if p.exists():
                    p.unlink()
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"## ❌ 视频 {i+1} 失败: {video['desc']}\n\n")
                f.write(f"- 视频ID: {video['id']}\n- 错误: {e}\n\n---\n\n")
            failed += 1

    # 最终清理：确保所有临时文件都已删除
    for video in VIDEOS:
        for ext in ['.mp4', '.mp3']:
            tmp = Path(tempfile.gettempdir()) / f"dy_{video['id']}{ext}"
            if tmp.exists():
                tmp.unlink()
                print(f"🧹 清理残留: {tmp}")

    print(f"\n{'='*50}")
    print(f"🎉 批量处理完成!")
    print(f"  ✅ 成功: {success}")
    print(f"  ❌ 失败/跳过: {failed}")
    print(f"  📁 报告: {output_file}")
    print(f"TRANSCRIPTION_PATH:{output_file}")

if __name__ == "__main__":
    main()
