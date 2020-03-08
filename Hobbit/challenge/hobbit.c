#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/binfmts.h>
#include <linux/mm.h>
#include <linux/random.h>
#include <linux/ptrace.h>
#include <linux/sched/task_stack.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/string.h>

static int load_hobbit_binary(struct linux_binprm*);
static int __init module_initialize(void);
static void __exit module_cleanup(void);

static struct linux_binfmt hobbit_format = {
  .module = THIS_MODULE,
  .load_binary  = load_hobbit_binary,
};

typedef struct __attribute__((packed)) {
  char magic[8];
  char data_key[0x10];
  char text_key[0x10];
  unsigned int data_size;
  void *data_addr;
  unsigned int text_size;
  void *text_addr;
} Hobbit;

static unsigned long randomize_stack_top(unsigned long stack_top)
{
	unsigned long random_variable = 0;
	if (current->flags & PF_RANDOMIZE) {
		random_variable = get_random_long();
		random_variable &= STACK_RND_MASK;
		random_variable <<= PAGE_SHIFT;
	}
	return PAGE_ALIGN(stack_top) + random_variable;
}

void dilly_dally(unsigned char *a, unsigned char *b) {
  *a ^= *b;
  *b ^= *a;
  *a ^= *b;
}

int pickup(unsigned char *key, unsigned char *S) {
  int i, j;
  for(i = 0; i < 0x100; i+=4) {
    for(j = 0; j < 4; j++) {
      S[i+j] = i+j;
    }
  }
  j = 0;
  for(i = 0; i < 0x100; i++) {
    j = (j + S[i] + key[i & 0xf]) & 0xff;
    dilly_dally(&S[i], &S[j]);
  }
  return 0;
}

int adjust(unsigned char *S,
           unsigned char *plaintext,
           unsigned char *ciphertext,
           int len) {
  int n, rnd;
  int i = 0;
  int j = 0;
  for(n = 0; n < len; n++) {
    i = (i + 1) & 0xff;
    j = (j + S[i]) & 0xff;
    dilly_dally(&S[i], &S[j]);
    rnd = S[(S[i] + S[j]) & 0xff];
    ciphertext[n] = rnd ^ plaintext[n];
  }
  return 0;
}

int wear_ring(char *key, char *plaintext, char *ciphertext, int len) {
  unsigned char S[0x100];
  pickup(key, S);
  adjust(S, plaintext, ciphertext, len);
  return 0;
}

int The_Load_of_the_Rings(unsigned long base, char *_cipher, int len, char *key)
{
  long retval;
  unsigned char *plain, *cipher;

  // Load data
  if ((retval = vm_mmap(NULL, base, len, VM_READ | VM_WRITE | VM_EXEC, 2, 0)) == -EINVAL)
    return retval;
  if ((plain = kmalloc(len, GFP_KERNEL)) == NULL)
    return -EINVAL;
  if ((cipher = kmalloc(len, GFP_KERNEL)) == NULL)
    return -EINVAL;
  memcpy(cipher, _cipher, len);

  // Decrypt section
  wear_ring(key, cipher, plain, len);

  // Copy to userland
  if (copy_to_user((void*)base, plain, len)) {
    kfree(plain);
    kfree(cipher);
    return -EINVAL;
  }

  kfree(plain);
  kfree(cipher);
  return 0;
}

static int load_hobbit_binary(struct linux_binprm *bprm)
{
  loff_t pos;
  long retval;
  unsigned long data_base, text_base;
  unsigned char *data, *text;
  struct pt_regs *regs;
  Hobbit *hobbit = (Hobbit*)bprm->buf;

  // Check magic
  if (*(unsigned long*)hobbit->magic != 0x0201544942424f48)
    return -ENOEXEC;

  // Delete old context
  retval = flush_old_exec(bprm);
  if (retval)
    return retval;

  // Setup new context
  setup_new_exec(bprm);
  install_exec_creds(bprm);
  retval = setup_arg_pages(bprm, randomize_stack_top(STACK_TOP), 0);
  if (retval < 0)
    return retval;

  // Setup data section
  data_base = (unsigned long)hobbit->data_addr & 0xffffffffffff0000;
  if ((data = kmalloc(hobbit->data_size, GFP_KERNEL)) == NULL)
    return -EINVAL;
  pos = sizeof(Hobbit);
  kernel_read(bprm->file, data, hobbit->data_size, &pos);
  if (The_Load_of_the_Rings(data_base,
                            data,
                            hobbit->data_size,
                            hobbit->data_key) < 0)
    return -EINVAL;

  // Setup text section
  text_base = (unsigned long)hobbit->text_addr & 0xffffffffffff0000;
  if ((text = kmalloc(hobbit->text_size, GFP_KERNEL)) == NULL)
    return -EINVAL;
  pos = sizeof(Hobbit) + hobbit->data_size;
  kernel_read(bprm->file, text, hobbit->text_size, &pos);
  if (The_Load_of_the_Rings(text_base,
                            text,
                            hobbit->text_size,
                            hobbit->text_key) < 0)
    return -EINVAL;

  // Install
  set_binfmt(&hobbit_format);

  // Setup context
  current->mm->end_code    = text_base + hobbit->text_size;
  current->mm->start_code  = text_base;
  current->mm->start_data  = data_base;
  current->mm->end_data    = data_base + hobbit->data_size;
  current->mm->start_stack = bprm->p;

  // Run!
  regs = current_pt_regs();
  finalize_exec(bprm);
  start_thread(regs, text_base, bprm->p);
  return 0;
}

static int __init module_initialize(void)
{
  register_binfmt(&hobbit_format);
  return 0;
}

static void __exit module_cleanup(void)
{
  unregister_binfmt(&hobbit_format);
}

core_initcall(module_initialize);
module_exit(module_cleanup);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ptr-yudai");
MODULE_DESCRIPTION("zer0pts CTF 2020 HOBBIT");
