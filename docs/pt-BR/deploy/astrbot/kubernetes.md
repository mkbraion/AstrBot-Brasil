# Implantar o AstrBot com Kubernetes

> [!WARNING]
> Você pode implantar o AstrBot em uma configuração de alta disponibilidade usando Kubernetes (K8s), permitindo que o sistema se recupere automaticamente de falhas.
>
> Como o projeto utiliza atualmente um banco de dados SQLite, esta implantação não oferece suporte à escalabilidade horizontal com várias réplicas. Além disso, se você usar o modo Sidecar, preste atenção à persistência do estado de login do NapCat.
>
> Este tutorial pressupõe que o `kubectl` esteja instalado e configurado e que você consiga se conectar ao seu cluster K8s.

## Pré-requisitos

Antes de começar, confirme que seu cluster Kubernetes atende às seguintes condições:

1. **StorageClass padrão:** usada para criar dinamicamente um `PersistentVolumeClaim` (PVC). Você pode verificar a configuração com `kubectl get sc`. Se não houver uma classe padrão, será necessário criar manualmente um `PersistentVolume` (PV) ou instalar um plugin de armazenamento correspondente, como `nfs-client-provisioner`.
2. **Acesso à rede:** confirme que os nós do cluster conseguem baixar imagens de `docker.io` ou do repositório de imagens que você especificou.

## Métodos de implantação

Oferecemos duas opções:

- **Implantação integrada (modo Sidecar):** implanta o AstrBot e o NapCat no mesmo Pod. Recomendada para contas pessoais do QQ.
- **Implantação independente:** implanta somente o AstrBot. É adequada para outras plataformas ou quando você deseja gerenciar o NapCat separadamente.

---

### Método 1: implantar com NapCatQQ (Sidecar)

Os arquivos deste método ficam no diretório `k8s/astrbot_with_napcat`.

#### 1. Implantar

~~~bash
# 1. Criar o namespace
kubectl apply -f k8s/astrbot_with_napcat/00-namespace.yaml

# 2. Criar o Persistent Volume Claim
# Observação: astrbot-data-shared-pvc requer o modo de acesso ReadWriteMany (RWX).
# Se o cluster não oferecer suporte a RWX, configure um armazenamento compartilhado, como NFS, e altere storageClassName em 01-pvc.yaml.
kubectl apply -f k8s/astrbot_with_napcat/01-pvc.yaml

# 3. Implantar a aplicação
kubectl apply -f k8s/astrbot_with_napcat/02-deployment.yaml
~~~

#### 2. Expor o serviço (escolha uma opção)

- **Opção A: NodePort**

  ~~~bash
  kubectl apply -f k8s/astrbot_with_napcat/03-service-nodeport.yaml
  ~~~

  O serviço será exposto pelo IP de um nó e por uma porta atribuída automaticamente pelo Kubernetes. Para descobrir a porta, execute:

  ~~~bash
  kubectl get svc -n astrbot-ns
  ~~~

  Na saída, localize a coluna `PORT(S)` dos serviços `astrbot-webui-svc` e `napcat-web-svc`. O formato é `<internal-port>:<NodePort>/TCP`. Por exemplo, se aparecer `8080:30185/TCP`, o endereço de acesso será `http://<NodeIP>:30185`.

- **Opção B: LoadBalancer**

  Se o cluster oferecer suporte a serviços do tipo `LoadBalancer` (geralmente disponibilizados por provedores de nuvem), você poderá usar este método.

  ~~~bash
  kubectl apply -f k8s/astrbot_with_napcat/04-service-loadbalancer.yaml
  ~~~

  Depois da execução, consulte o IP externo atribuído (`EXTERNAL-IP`) com `kubectl get svc -n astrbot-ns`.

#### 3. Configurar a conexão

Como o AstrBot e o NapCat estão no mesmo Pod, eles podem se comunicar diretamente por meio de `localhost`.

1. **Adicionar uma plataforma de mensagens no AstrBot:**
   - Abra a WebUI do AstrBot e selecione `Platforms` → `Add Adapter`.
   - **Categoria da plataforma de mensagens:** `aiocqhttp`
   - **Nome do bot:** `napcat` (ou outro nome personalizado).
   - **Host do WebSocket reverso:** `0.0.0.0`
   - **Porta do WebSocket reverso:** `6199`
   - Salve a configuração.

2. **Configurar o cliente WebSocket no NapCat:**
   - Abra a WebUI do NapCat e selecione `Settings` → `Reverse WS` → `Add`.
   - **Habilitado:** ligado.
   - **URL:** `ws://localhost:6199/ws`
   - **Formato da mensagem:** `Array`
   - Salve a configuração.

---

### Método 2: implantar somente o AstrBot (uso geral)

Os arquivos deste método ficam no diretório `k8s/astrbot`.

#### 1. Implantar

~~~bash
# 1. Criar o namespace
kubectl apply -f k8s/astrbot/00-namespace.yaml

# 2. Criar o Persistent Volume Claim
kubectl apply -f k8s/astrbot/01-pvc.yaml

# 3. Implantar a aplicação
kubectl apply -f k8s/astrbot/02-deployment.yaml
~~~

#### 2. Expor o serviço (escolha uma opção)

- **Opção A: NodePort**

  ~~~bash
  kubectl apply -f k8s/astrbot/03-service-nodeport.yaml
  ~~~

  O serviço será exposto pelo IP de um nó e por uma porta atribuída automaticamente pelo Kubernetes. Para descobrir a porta, execute:

  ~~~bash
  kubectl get svc -n astrbot-standalone-ns
  ~~~

  Na saída, localize a coluna `PORT(S)` do serviço `astrbot-webui-svc`. O formato é `<internal-port>:<NodePort>/TCP`. Por exemplo, se aparecer `8080:30185/TCP`, o endereço de acesso será `http://<NodeIP>:30185`.

- **Opção B: LoadBalancer**

  ~~~bash
  kubectl apply -f k8s/astrbot/04-service-loadbalancer.yaml
  ~~~

  Depois da execução, consulte o IP externo atribuído (`EXTERNAL-IP`) com `kubectl get svc -n astrbot-standalone-ns`.

---

## Configuração avançada

### Espelho de imagens (para usuários na China continental)

Se você tiver dificuldade para baixar as imagens `soulter/astrbot:latest` ou `mlikiowa/napcat-docker:latest`, edite manualmente o arquivo `02-deployment.yaml` correspondente e substitua o campo `image` por um endereço de espelho local. Por exemplo:

~~~yaml
# Exemplo:
# image: soulter/astrbot:latest
# Substitua por:
image: m.daocloud.io/docker.io/soulter/astrbot:latest
~~~

### Habilitar o executor de código Docker Sandbox

Se precisar usar o executor de código em sandbox, será necessário montar o arquivo de socket do Docker no Pod.

Edite o arquivo `02-deployment.yaml` e adicione `volumes` e `volumeMounts` em `spec.template.spec`:

1. **Adicione o trecho a seguir à lista `volumeMounts` do contêiner `astrbot`:**

   ~~~yaml
   - name: docker-sock
     mountPath: /var/run/docker.sock
   ~~~

2. **Adicione o trecho a seguir à lista `spec.template.spec.volumes`:**

   ~~~yaml
   - name: docker-sock
     hostPath:
       path: /var/run/docker.sock
       type: Socket
   ~~~

> [!WARNING]
> Montar o socket do Docker em um Pod representa um risco de segurança. Certifique-se de compreender as implicações antes de fazer isso.

## Consultar os logs

- **Modo de implantação Sidecar:**

  ~~~bash
  # Consultar os logs do AstrBot
  kubectl logs -f -n astrbot-ns deployment/astrbot-stack -c astrbot

  # Consultar os logs do NapCat
  kubectl logs -f -n astrbot-ns deployment/astrbot-stack -c napcat
  ~~~

- **Modo de implantação independente:**

  ~~~bash
  kubectl logs -f -n astrbot-standalone-ns deployment/astrbot-standalone
  ~~~

## 🎉 Tudo pronto!

Depois de implantar e expor o serviço, você poderá acessar o painel de administração do AstrBot pelo IP e pela porta correspondentes.

> Novos usuários devem usar a senha aleatória exibida nos logs de inicialização no primeiro acesso. Use o nome de usuário mostrado nos logs (geralmente `astrbot`) e altere a senha depois de entrar.
