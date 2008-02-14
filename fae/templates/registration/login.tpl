<h1><?= $title ?></h1>

<?php if ($session->isLoggedIn()): ?>
<p>You are already logged in as <strong><?= $session->getUsername() ?></strong>!</p>
<p>To review your account information, please select <a href="myaccount.php">My Account</a>.</p>

<?php else: ?>
<?= $form->error("registration") ?>
<form action="<?= $action ?>" method="post">
<fieldset style="width:50%">
<div style="margin-top: 0.375em">
<label>Username:<br/>
<input type="text" name="user" id="focus" maxlength="30" value="<?= $form->value('user') ?>"/>&nbsp;&nbsp;<?= $form->error('user') ?>
</label>
</div>

<div style="margin-top: 0.75em">
<label>Password:<br/>
<input type="password" name="pass" maxlength="30" value="<?= $form->value('pass') ?>"/>&nbsp;&nbsp;<?= $form->error('pass'); ?>
</label>
</div>

<div style="margin-top: 0.75em; margin-left: -3px">
<label>
<input type="checkbox" name="remember" <? if ($form->value('remember') != ''){ echo "checked"; } ?>/>
Remember me
</label>
</div>

<div style="margin-top: 0.75em; margin-bottom: 0.375em">
<input type="hidden" name="sublogin" value="1"/>
<label title="Login"><input type="submit" value="Login"/></label>
</div>
</fieldset>

<div>
<p>Not a member? [<a href="<?= construct_href('register.php') ?>">Register for a free account!</a>]</p>
<p>[<a href="<?= construct_href('forgotpass.php') ?>">Forgot Password?</a>]</p>
</div>

</form>
<?php endif; ?>
