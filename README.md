##Слава Украине!

###Установка докера в линукс системе одной строкой:

```shell
sudo apt update && sudo apt install -y git mcedit apt-transport-https ca-certificates curl software-properties-common && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" && sudo apt update && apt-cache policy docker-ce && sudo apt install -y docker-ce && sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose
```

###Теперь скачиваем ддосер

```shell
git clone https://github.com/torosyatko/dosya.git
```

####Переходим в папку и редактируем настройки
```shell
cd dosya
mv .env-example .env
```

Если хочется руками подкидывать ссылки тогда правим data/link.txt

```shell
mcedit data/link.txt
```

Если хочется прописать ссылку на подобным=й файл то правим .env 


Предложения по улучшению: https://t.me/svyatkss