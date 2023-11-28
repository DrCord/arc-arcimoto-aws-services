# Changelog

<!--next-version-placeholder-->

## v1.1.7 (2022-12-01)
### Fix
* **pipeline:** Create directory for release output earlier ([`da9b955`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/da9b955dc485b779a675c67c21c1afec5a94ed8e))
* **pipeline:** Determine version bump type via comparison ([`a88b429`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/a88b4293d2b02e04175b4eb09584c8804740b94a))

## v1.1.6 (2022-12-01)
### Fix
* **pipeline:** Add current flag to print-version commands ([`fa2bec8`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/fa2bec85d1c994949013e5a1e4ff986166e2bf6b))

## v1.1.5 (2022-12-01)
### Fix
* **pipeline:** Set commit message as string ([`6b088ac`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/6b088ac811b152afa3bbd0f25052daf189416936))

## v1.1.4 (2022-12-01)
### Fix
* **pipeline:** Access commit message body variable ([`57e19b5`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/57e19b5d0f56f3ee8e52f24b57e4fcc295e7cc19))

## v1.1.3 (2022-11-30)
### Fix
* **pipeline:** Use angular style in release publish commits ([`303a2fc`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/303a2fc3e309f2a08c6ccdd995f62e8613371420))
* **pipeline:** Do not backmerge if no release published ([`701e126`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/701e126696388c386e80d77dad210e1ff522cf7b))

## v1.1.2 (2022-11-22)
### Fix
* **cognito:** Remove erroneous parameter from function call ([`0787bec`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/0787becb40c268c74e77b2404a9df6c1b15046cb))

## v1.1.1 (2022-11-15)
### Fix
* **pipeline:** Handle automatic pr without conflicts ([`57cbe21`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/57cbe2197b319f57987bc2ccbafe64efc68a13d3))
* **pipeline:** Get correct version for prod email release ([`1245dfa`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/1245dfaae79722f714e439850d3cbd6fd3a34e94))
* **pipeline:** Automate pr to ses utility ([`3e4bdfc`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/3e4bdfcdb6fae8d174159ebf8361ea4764caf828))

## v1.1.0 (2022-11-15)
### Feature
* **ses:** Add ses functionality ([`48811ad`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/48811ad619363361f031bd338d25154703ab65c8))

## v1.0.2 (2022-11-01)
### Fix
* **pipeline:** Set root pip cache location for auto-use ([`1ee66ab`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/1ee66ab4f098d3bb3b50e5c2102c160d4a7a0d18))

### Documentation
* **pipeline:** Ammend comment to make sense ([`0cfcfc8`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/0cfcfc8ec879d8a5ac0804d72ddb7880288781fc))

## v1.0.1 (2022-10-28)
### Fix
* Merge conflict ([`c1862d4`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/c1862d4b8cb82d79c7a9f3ecf06fc2ca335dab7e))

### Documentation
* Note how version is automatically maintained ([`db6308a`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/db6308a5b339ee2b3b4c34992f242346aeaee528))

## v1.0.0 (2022-10-28)


## v0.1.2 (2022-10-28)
### Fix
* **pipeline:** Fail step if bb token output empty ([`041a4d9`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/041a4d93d1add6465d7200d6bfad8718086f3aa6))

## v0.1.1 (2022-10-28)
### Fix
* **pipeline:** Add missing gulpfile ([`e76c5a9`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/e76c5a962231d0a41f109350f53e3d79bfce8148))

### Documentation
* **pipeline:** Include info about auto-PRs to dependent repos ([`2d636ab`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/2d636ab9081e394dc37dd7b32cd14c396319ad41))

## v0.1.0 (2022-10-26)
### Feature
* **pipeline:** BREAKING CHANGE: force initial major version bump ([`cd43d5b`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/cd43d5bc4c5b94e5a9c6ca86992fe116d08174d1))
* **pipeline:** Automatically publish new semantic release ([`36ae625`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/36ae625926b03ba730e652c7f6d163cf95e99dd4))

### Fix
* **pipeline:** Correct typos/other repo ref  in emails ([`38e0fa8`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/38e0fa8cc4655d9db5ff76d2e8fca0df53867fc6))
* **pipeline:** Correct email headers to show name of this repo ([`ff647b8`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/ff647b8c546ae45ed6cf19426a4f129812b0dac4))
* **bundle:** Don't append extra folder for layers ([`a06c744`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/a06c744af3e3e82b03a9001a55dda86b7a89304c))
* **secretsmanager:** Don't auto close connection in get_secret ([`46185bd`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/46185bd628f511c37481900a5df251a430fd0796))

### Documentation
* **readme:** Add info about using in bitbucket pipeline via ssh ([`0698514`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/069851455098b7c5146432316109aa71e61e72f2))
* Remove incorrect readme file ([`813f71e`](https://github.com/arcimotocode1/arcimoto-aws-services/commit/813f71e79dcc9c66f16d16ea93446e006991c54b))
